//!
//! \file
//!

//! \brief This is an example of how to build and run a schedule that compares two LPPMs

#include "include/Public.h"

using namespace lpm;

int main(int argc, char **argv)
{
	LPM* lpm = LPM::GetInstance();

	Parameters::GetInstance()->AddUsersRange(2, 5); // {2, 3, 4, 5}
	Parameters::GetInstance()->SetTimestampsRange(1, 24);
	Parameters::GetInstance()->SetLocationstampsRange(1, 8);

	Log::GetInstance()->SetEnabled(true);
	Log::GetInstance()->SetOutputFileName("output");

	// create the builder object (we name the schedule which will be created: "Simple LPPM comparison schedule")
	ScheduleBuilder* builder = new ScheduleBuilder("Simple LPPM comparison schedule");

	// set the default inputs: we only give the knowledge file, for the rest, the default values will be used
	File contextFile("knowledge");
	VERIFY(builder->SetInputs(&contextFile) == true);

	// create and set the application
	ApplicationOperation* application = new DefaultApplicationOperation(0.3);
	VERIFY(builder->SetApplicationOperation(application) == true);

	// release ownership so that the schedule is the only owner of the operation instance
	application->Release();

	// create the LPPMs
	LPPMOperation* lppms[] = { new DefaultLPPMOperation(1, 0.1, UniformSelection, 0.0), 
					new DefaultLPPMOperation(1, 0.0, UniformSelection, 0.1) };

	// branch the schedule (one branch per LPPM)
	unsigned short branches = 2;
	VERIFY(builder->ForkSchedule(branches) == true);

	for(unsigned short branchIdx = 0; branchIdx < branches; branchIdx++)
	{
		// get the branch's schedule builder
		 ScheduleBuilder* branchBuilder = builder->GetBranchScheduleBuilder(branchIdx);

		 // get and set the LPPM
		 LPPMOperation* lppm = lppms[branchIdx];
		 VERIFY(branchBuilder->SetLPPMOperation(lppm) == true);

		 // create and set the attack
		 AttackOperation* attack = new StrongAttackOperation();
		 VERIFY(branchBuilder->SetAttackOperation(attack) == true);

		 // set the metric
		 VERIFY(branchBuilder->SetMetricType(Distortion) == true);

		 // release ownership so that the schedule is the only owner of the operations' instances
		 lppm->Release();
		 attack->Release();
	 }

	Schedule* schedule = builder->GetSchedule();
	VERIFY(schedule != NULL);

	// Free the builder (this essentially severs the tie between the builder and the schedule)
	delete builder;

	std::cout << schedule->GetDetailString() << endl ; // print a description of the schedule

	std::cout << "Running schedule...";
	 
	File input("actual.trace");
	if(lpm->RunSchedule(schedule , &input , "output") == false) // run the schedule
	{
		std::cout << Errors::GetInstance()->GetLastErrorMessage() << endl ; // print the error message
		return -1;
	}

	std::cout << " done!" << endl;

	schedule->Release(); // release the schedule object (since it is no longer needed)

	return 0;
}
