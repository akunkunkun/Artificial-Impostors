//!
//! \file
//!

//! \brief This is an example of constructing the adversary knowledge

#include "include/Public.h" // the public header (Public.h) is the only header that should be included when linking with the library

using namespace lpm; // using the namespace allows to drop the lpm:: prefix in front of classes, structs etc...

int main(int argc, char **argv)
{
	LPM* lpm = LPM::GetInstance();	// get a pointer to the LPM engine (core class)

	Parameters::GetInstance()->AddUsersRange(2, 5);
	Parameters::GetInstance()->RemoveUsersRange(3, 4); // consider only users 2 and 5 (i.e. {2, 3, 4, 5} \ {3, 4})

	ull timestamps = 24 * 7; // 168
	Parameters::GetInstance()->SetTimestampsRange(1, timestamps); // consider only timestamps 1, 2, 3, ..., 168
	Parameters::GetInstance()->SetLocationstampsRange(1, 8); // consider only locationstamps 1, 2, 3, 4, 5, 6, 7, 8

	Log::GetInstance()->SetEnabled(true); // [optional] enable the logging facilities
	Log::GetInstance()->SetOutputFileName("output"); // [optional] set the log file name (here: output.log)

	File learningTraceFile("learning.trace", true); // the learning trace file (in the current directory), read-only mode
	File outputKC("knowledge", false); // the name of the output (the knowledge), write mode

	KnowledgeInput knowledge;	// construct and fill in the knowledge input
	knowledge.transitionsFeasibilityFile = NULL;	// a NULL pointer as transitions feasibility file means users can go from any location to any location
	knowledge.transitionsCountFile = NULL;	// a NULL pointer as transitions count file means no transitions knowledge not encoded as learning trace
	knowledge.learningTraceFilesVector = vector<File*>();
	knowledge.learningTraceFilesVector.push_back(&learningTraceFile); // add a pointer to the learning trace file

	// simple time partitioning: one day partitioned into morning, afternoon, night
	ull dayLength = 24; // time instants in a day
	ull days = timestamps / dayLength; // a week

	const ull weeks = 1;
	TPNode* timePart = Parameters::GetInstance()->CreateTimePartitioning(1, weeks * days * dayLength); // partition a week

	TPNode* week = NULL;
	VERIFY(timePart->SliceOut(0, days * dayLength, weeks, &week) == true); // get the week

	TPNode* weekdays = NULL;
	VERIFY(week->SliceOut(0, dayLength, 5, &weekdays) == true); // get the week days (first 5 days)

	TPNode* weekend = NULL;
	VERIFY(week->SliceOut(5*dayLength, dayLength, 2, &weekend) == true); // get the weekend days

	// week days
	TimePeriod morningwd; morningwd.start = 7 * dayLength/24; morningwd.length=5 * dayLength/24; morningwd.id = 1; morningwd.dummy = false;
	TimePeriod afternoonwd; afternoonwd.start = 12 * dayLength/24; afternoonwd.length=7 * dayLength/24; afternoonwd.id = 2; afternoonwd.dummy = false;
	TimePeriod nightpart1; nightpart1.start = 0 * dayLength/24; nightpart1.length=7 * dayLength/24; nightpart1.id = 3; nightpart1.dummy = false;
	TimePeriod nightpart2; nightpart2.start = 19 * dayLength/24; nightpart2.length=5 * dayLength/24; nightpart2.id = 3; nightpart2.dummy = false;

	vector<TimePeriod> periods = vector<TimePeriod>();
	periods.push_back(morningwd);
	periods.push_back(afternoonwd);
	periods.push_back(nightpart1);
	periods.push_back(nightpart2);

	VERIFY(weekdays->Partition(periods) == true);

	// weekend (a single time period for each day)
	TimePeriod we; we.start = 0 * dayLength/24; we.length=24 * dayLength/24; we.id = 4; we.dummy = false;

	periods.clear();
	periods.push_back(we);

	VERIFY(weekend->Partition(periods) == true);

	// print out the time partitioning
	string str = "";
	VERIFY(timePart->GetStringRepresentation(str) == true);
	std::cout << "Time Partitioning:" << endl << str << endl;

	Parameters::GetInstance()->SetTimePartitioning(timePart); // set the time partitioning


	std::cout << "Starting Knowledge Construction" << endl;

	ull maxGSIterations = 100; // do at most 100 iterations of Gibbs sampling per user
	ull maxSeconds = 30; // and spend at most 30 sec per user (whichever occurs first).
	if(lpm->RunKnowledgeConstruction(&knowledge, &outputKC, maxGSIterations, maxSeconds) == false)
	{
		std::cout << Errors::GetInstance()->GetLastErrorMessage() << endl;	// display the error that occur and exit gracefully.
		return -1;
	}

	std::cout << "Done!" << endl;

	return 0;	// all went well
}
