//!
//! \file
//!

//! \brief This is an example of extending the tool by defining new Application and LPPM operations

#include "include/Public.h" // the public header (Public.h) is the only header that should be included when linking with the library

using namespace lpm; // using the namespace allows to drop the lpm:: prefix in front of classes, structs etc...

// new app
class BasicApplicationOperation : public ApplicationOperation
{
private:
	double exposeProb;

public:
	BasicApplicationOperation(double prob) : ApplicationOperation("BasicApplicationOperation"), exposeProb(prob) {}

	bool Filter(const Context* context, const ActualEvent* inEvent, ActualEvent** outEvent);
	double PDF(const Context* context, const ActualEvent* inEvent, const ActualEvent* outEvent) const;
};

bool BasicApplicationOperation::Filter(const Context* context, const ActualEvent* inEvent, ActualEvent** outEvent)
{
	if(context == NULL || inEvent == NULL || outEvent == NULL)
	{
		SET_ERROR_CODE(ERROR_CODE_INVALID_ARGUMENTS);
		return false;
	}
	
	double randomSample = RNG::GetInstance()->GetUniformRandomDouble();
	if(randomSample <= exposeProb)
	{
		*outEvent = new ExposedEvent(*inEvent); // expose
	}
	else
	{
		*outEvent = new ActualEvent(*inEvent); // do *not* expose
	}

	return true;

}

double BasicApplicationOperation::PDF(const Context* context, const ActualEvent* inEvent, const ActualEvent* outEvent) const
{
	VERIFY(outEvent != NULL);

	if(inEvent->GetUser() != outEvent->GetUser() ||
		inEvent->GetTimestamp() != outEvent->GetTimestamp() ||
		inEvent->GetLocationstamp() != outEvent->GetLocationstamp())
	{
		return 0.0; // The probability of modifying the event (i.e. the user id, timestamp or locationstamp) is 0.0 ! */
	}

	return (outEvent->GetType() == Exposed) ? exposeProb : 1.0 - exposeProb;
}

// new LPPM

class HidingLPPMOperation : public LPPMOperation
{
private:
	double hidingProb;
public:
	HidingLPPMOperation(double prob) : LPPMOperation("HidingLPPMOperation"), hidingProb(prob) {};

	bool Filter(const Context* context, const ActualEvent* inEvent, ObservedEvent** outEvent);
	double PDF(const Context* context, const ActualEvent* inEvent, const ObservedEvent* outEvent) const;
};

bool HidingLPPMOperation::Filter(const Context* context, const ActualEvent* inEvent, ObservedEvent** outEvent)
{
	if(context == NULL || inEvent == NULL || outEvent == NULL)
	{
		SET_ERROR_CODE(ERROR_CODE_INVALID_ARGUMENTS);
		return false;
	}

	VERIFY(inEvent->GetType() == Actual || inEvent->GetType() == Exposed);

	ull pseudonym = GetPseudonym(inEvent->GetUser()); // get the pseudonym for that user from the random permutation

	ObservedEvent* event = *outEvent = new ObservedEvent(pseudonym);
	ull timestamp = inEvent->GetTimestamp();
	event->AddTimestamp(timestamp);

	ull minLoc = 0; ull maxLoc = 0; // get minLoc and maxLoc
	VERIFY(Parameters::GetInstance()->GetLocationstampsRange(&minLoc, &maxLoc) == true);

	ull location = inEvent->GetLocationstamp();

	if(inEvent->GetType() == Actual) // event is *not* exposed (do nothing)
	{
		; // do nothing
	}
	else
	{
		// event is exposed (either we hide the location, or we do not)

		double randomSample = RNG::GetInstance()->GetUniformRandomDouble();
		if(randomSample <= hidingProb)
		{
			; // do nothing (i.e. hide the location)
		}
		else
		{
			event->AddLocationstamp(location); // add the original location (i.e. do not hide the location)
		}
	}

	return true;
}

double HidingLPPMOperation::PDF(const Context* context, const ActualEvent* inEvent, const ObservedEvent* outEvent) const
{

	VERIFY(context != NULL && inEvent != NULL && outEvent != NULL);

	ull minLoc = 0; ull maxLoc = 0;
	VERIFY(Parameters::GetInstance()->GetLocationstampsRange(&minLoc, &maxLoc) == true);
	ull trueTimestamp = inEvent->GetTimestamp();

	set<ull> timestamps = set<ull>();
	outEvent->GetTimestamps(timestamps);

	if(timestamps.size() != 1 || timestamps.find(trueTimestamp) == timestamps.end()) { return 0.0; /* This LPPM does not modify the timestamps */}

	ull trueLoc = inEvent->GetLocationstamp();

	set<ull> locs = set<ull>();
	outEvent->GetLocationstamps(locs);

	ull locsInSet = locs.size();

	if(locsInSet >= 2) { return 0.0; } /* This LPPM *never* outputs events with more than one location is the locationstamp set. */

	if(locsInSet == 1)
	{
		ull loc = *locs.begin();

		if(loc != trueLoc) { return 0.0; } // this LPPM can only hide the "true" location, it *never* distorts it
	}

	if(inEvent->GetType() == Actual) // event is *not* exposed (i.e. we have to return pdf conditional upon the event *not* being exposed)
	{
		return (locsInSet == 0) ? 1.0 : 0.0; /* When the event is *not* exposed, the locationstamps set is always empty! */
	}
	else  // event is exposed (i.e. we have to return pdf conditional upon the event being exposed)
	{
		return (locsInSet == 1) ? 1.0 - hidingProb : hidingProb; // hide with probability 'hidingProb'
	}

	return 0.0;
}

// main

int main(int argc, char **argv)
{
	LPM* lpm = LPM::GetInstance();	// get a pointer to the LPM engine (core class)

	Parameters::GetInstance()->AddUsersRange(2, 5); // consider only simulated users ID 2, 3, 4, 5

	Parameters::GetInstance()->SetTimestampsRange(1, 24);  // consider only timestamps 1, 2, 3, ..., 23, 24
	Parameters::GetInstance()->SetLocationstampsRange(1, 8); // consider only locationstamps 1, 2, 3, 4, 5, 6, 7, 8

	Log::GetInstance()->SetEnabled(true); // [optional] enable the logging facilities
	Log::GetInstance()->SetOutputFileName("output"); // [optional] set the log file name (here: output.log)

	// Tweak the template's parameters
	BasicApplicationOperation* basicApp = new BasicApplicationOperation(0.3); // create an instance with exposeProb = 0.3
	SimpleScheduleTemplate::GetInstance()->SetApplicationOperation(basicApp);
	basicApp->Release(); // release the App instance => give exclusive ownership of the object to the schedule

	HidingLPPMOperation* hidingLPPM = new HidingLPPMOperation(0.2); // create an instance with hidingProb = 0.2
	SimpleScheduleTemplate::GetInstance()->SetLPPMOperation(hidingLPPM);
	hidingLPPM->Release(); // release the LPPM instance => give exclusive ownership of the object to the schedule

	SimpleScheduleTemplate::GetInstance()->SetAttackParameter(Strong);
	SimpleScheduleTemplate::GetInstance()->SetMetricParameters(Anonymity);

	File knowledge("knowledge");
	Schedule* schedule = SimpleScheduleTemplate::GetInstance()->BuildSchedule(&knowledge, "simple"); // build the schedule

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
