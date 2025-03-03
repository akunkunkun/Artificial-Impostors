//!
//! \file
//!

//! \brief This is an example of saving the observed traces from LPPM into file

#include "include/Public.h"

using namespace lpm;

int main(int argc, char **argv)
{
	LPM* lpm = LPM::GetInstance();

	Parameters::GetInstance()->AddUsersRange(2, 5);
	Parameters::GetInstance()->SetTimestampsRange(1, 24);
	Parameters::GetInstance()->SetLocationstampsRange(1, 8);

	Log::GetInstance()->SetEnabled(true);
	Log::GetInstance()->SetOutputFileName("output");

	// create the builder object
	ScheduleBuilder* builder = new ScheduleBuilder("Stop-After-LPPM schedule");

	// set the default inputs: we only give the knowledge file, for the rest, the default values will be used
	File contextFile("knowledge");
	VERIFY(builder->SetInputs(&contextFile) == true);

	// create and set the application
	ApplicationOperation* app = new DefaultApplicationOperation(0.5, Basic);
	VERIFY(builder->SetApplicationOperation(app) == true);
	app->Release(); // release ownership so that the schedule is the only owner of the operation instance

	// create and set the LPPM
	LPPMOperation* lppm = new DefaultLPPMOperation(1, 0.1, GeneralStatisticsSelection, 0.1);
	VERIFY(builder->SetLPPMOperation(lppm) == true);
	lppm->Release(); // release ownership so that the schedule is the only owner of the operation instance

	VERIFY(builder->InsertOutputOperation() == true); // insert intermediary output

	Schedule* schedule = builder->GetSchedule(); // retrieve the schedule right now (=> schedule stops after LPPM).
	VERIFY(schedule != NULL);

	// Free the builder (this essentially severs the tie between the builder and the schedule)
	delete builder;

	std::cout << schedule->GetDetailString() << endl ; // print a description of the schedule

	std::cout << "Running schedule...";
	 
	File input("actual.trace");
	if(lpm->RunSchedule(schedule , &input, "output") == false) // run the schedule
	{
		std::cout << Errors::GetInstance()->GetLastErrorMessage() << endl ; // print the error message
		return -1;
	}

	std::cout << " done!" << endl;

	schedule->Release(); // release the schedule object (since it is no longer needed)

	return 0;
}
