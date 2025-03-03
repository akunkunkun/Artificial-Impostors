//! \file

// ... this piece of code could be placed inside Filter() or PDF() ...

ull minLoc = 0; ull maxLoc = 0; // retrieve the location parameters
VERIFY(Parameters::GetInstance()->GetLocationstampsRange(&minLoc, &maxLoc) == true);
ull numLoc = maxLoc - minLoc + 1;

ull user = inEvent->GetUser(); // get the user ID
ull loc = inEvent->GetLocationstamp(); // get the locationstamp

UserProfile* profile = NULL; // retrieve the profile for user
VERIFY(context->GetUserProfile(user, &profile) == true);

double* transitionMatrix = NULL; // retrieve the transition matrix
VERIFY(profile->GetTransitionMatrix(&transitionMatrix) == true && transitionMatrix != NULL);

double* steadystateVector = NULL; // retrieve the steady-state vector
VERIFY(profile->GetSteadyStateVector(&steadystateVector) == true && steadystateVector  != NULL);

ull locIndex = loc - minLoc; // compute columnIndex
ull entryIndex = GET_INDEX(locIndex, locIndex, numLoc); // the GET_INDEX macro takes 3 parameters: rowIndex, columnIndex, numColumns

double transitionLikelihood = transitionMatrix[entryIndex]; // transition probability of going from location loc to loc in one time instance

double presenceProbability = steadystateVector[locIndex]; // steady-state probability of being at location loc.

// ...
