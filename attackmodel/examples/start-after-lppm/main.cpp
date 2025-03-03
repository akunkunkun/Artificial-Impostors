//!
//! \file
//!

//! \brief This is an example of a schedule that runs an attack on a previously generated observed trace

#include "include/Public.h"

using namespace lpm;

int main(int argc, char **argv)
{
	LPM* lpm = LPM::GetInstance();

	Parameters::GetInstance()->AddUsersRange(1, 10);
	Parameters::GetInstance()->SetTimestampsRange(1, 24);
	Parameters::GetInstance()->SetLocationstampsRange(1, 8);

	Log::GetInstance()->SetEnabled(true);
	Log::GetInstance()->SetOutputFileName("output");

	// create the builder object
	ScheduleBuilder* builder = new ScheduleBuilder("Start-After-LPPM schedule");

	File contextFile("knowledge");

	// create instances of the application and the LPPM used, so that we can retrieve their PDFs.
	// note that in this case, we must *not* release ownership of these objects before we're done running the schedule
	ApplicationOperation* app = new DefaultApplicationOperation(0.5, Basic);
	LPPMOperation* lppm = new DefaultLPPMOperation(1, 0.1, GeneralStatisticsSelection, 0.1);

	// retrieve the application and LPPM PDFs
	FilterFunction* applicationPDF = dynamic_cast<FilterFunction*>(app);
	FilterFunction* lppmPDF = dynamic_cast<FilterFunction*>(lppm);

	SchedulePosition startPos = ScheduleInvalidPosition;
	File actualTraceFile("actual.trace");

	// set the inputs: we give the knowledge file, the actual trace file, the application and LPPM PDFs 
	// (for the rest, the default values will be used). 
	VERIFY(builder->SetInputs(&contextFile, &actualTraceFile, &startPos, applicationPDF, lppmPDF) == true);

	// check that we provided the inputs correctly (i.e. we make sure the builder correctly inferred that
	// we want our schedule to start after the LPPM operation: ScheduleBeforeAttackOperation <=> after LPPM operation)
	VERIFY(startPos == ScheduleBeforeAttackOperation);

	// create and set the attack
	AttackOperation* attack = new StrongAttackOperation();
	VERIFY(builder->SetAttackOperation(attack) == true);
	attack->Release(); // release ownership

	// set the metric type
	VERIFY(builder->SetMetricType(Distortion) == true);

	Schedule* schedule = builder->GetSchedule(); // retrieve the schedule
	VERIFY(schedule != NULL);

	// Free the builder (this essentially severs the tie between the builder and the schedule)
	delete builder;
	 
	std::cout << schedule->GetDetailString() << endl; // print a description of the schedule

	std::cout << "Running schedule...";

	// because the schedule starts after the LPPM, the input to RunSchedule is an observed trace !
	File input("observed.trace"); 
	if(lpm->RunSchedule(schedule , &input, "output") == false) // run the schedule
	{
		std::cout << Errors::GetInstance()->GetLastErrorMessage() << endl ; // print the error message
		return -1;
	}

	std::cout << " done!" << endl;

	schedule->Release(); // release the schedule object (since it is no longer needed)

	app->Release(); // it is now safe to release the application and LPPM instances
	lppm->Release();

	return 0;
}
