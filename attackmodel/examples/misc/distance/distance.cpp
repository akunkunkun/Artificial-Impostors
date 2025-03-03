//! \file

class AbsoluteLocationstampDistance : public MetricDistance
{
	virtual double ComputeDistance(ull firstLocation, ull secondLocation) const;
};

double AbsoluteLocationstampDistance::ComputeDistance(ull firstLocation, ull secondLocation) const
{
	if(firstLocation == secondLocation) { return 0.0; }
	return ABS((double)firstLocation - (double)secondLocation);
}

// ...
// ...

MetricDistance* myDistanceFunction = new AbsoluteLocationstampDistance();
VERIFY(builder->SetMetricType(Distortion, myDistanceFunction) == true);

// ...
