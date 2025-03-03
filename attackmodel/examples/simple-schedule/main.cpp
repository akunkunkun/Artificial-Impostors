//!
//! \file
//!

//! \brief This is an example of running a simple schedule that includes an Application, a LPPM, an Attack, and a Metric

#include "include/Public.h" // the public header (Public.h) is the only header that should be included when linking with the library

using namespace lpm; // using the namespace allows to drop the lpm:: prefix in front of classes, structs etc...

int main(int argc, char **argv)
{
	LPM* lpm = LPM::GetInstance();	// get a pointer to the LPM engine (core class)

	Parameters::GetInstance()->AddUsersRange(2, 2); // {2}
	Parameters::GetInstance()->AddUsersRange(5, 5); // -> {2, 5}

	Parameters::GetInstance()->SetTimestampsRange(7, 19);  // consider only timestamps 7, 8, ..., 18, 19
	Parameters::GetInstance()->SetLocationstampsRange(1, 8); // consider only locationstamps 1, 2, 3, 4, 5, 6, 7, 8

	Log::GetInstance()->SetEnabled(true); // [optional] enable the logging facilities
	Log::GetInstance()->SetOutputFileName("output"); // [optional] set the log file name (here: output.log)

	// Tweak the template's parameters
	SimpleScheduleTemplate::GetInstance()->SetApplicationParameters(Basic, 0.3);
	SimpleScheduleTemplate::GetInstance()->SetLPPMParameters(1, GeneralStatisticsSelection, 0.1, 0.05);
	SimpleScheduleTemplate::GetInstance()->SetAttackParameter(Strong);
	SimpleScheduleTemplate::GetInstance()->SetMetricParameters(Anonymity);

	File knowledge("knowledge");
	Schedule* schedule = SimpleScheduleTemplate::GetInstance()->BuildSchedule(&knowledge, "simple"); // build the schedule

	if(schedule == NULL) 
	{
		std::cout << Errors::GetInstance()->GetLastErrorMessage() << endl; // print the error message
		return -1;
	}

	std::cout << schedule->GetDetailString() << endl; // print a description of the schedule

	std::cout << "Running schedule...";

	File input("actual.trace");
	if(lpm->RunSchedule(schedule, &input, "output") == false) // run the schedule
	{
		std::cout << Errors::GetInstance()->GetLastErrorMessage() << endl; // print the error message
		return -1;
	}

	std::cout << " done!" << endl;

	schedule->Release(); // release the schedule object (since it is no longer needed)

	return 0;
}
