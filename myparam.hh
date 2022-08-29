#ifndef MYPARAM_HH
#define MYPARAM_HH

#include "G4VFastSimulationModel.hh"
#include "G4Step.hh"
#include "G4TouchableHandle.hh"
#include <vector>

class MyParamModel : public G4VFastSimulationModel
{
public:
  MyParamModel (G4String, G4Region*);
  MyParamModel (G4String);
  ~MyParamModel ();

  virtual G4bool IsApplicable(const G4ParticleDefinition&);
  virtual G4bool ModelTrigger(const G4FastTrack &);
  virtual void DoIt(const G4FastTrack&, G4FastStep&);

private:
  G4Step                         *fFakeStep;
  G4StepPoint                    *fFakePreStepPoint, *fFakePostStepPoint;
  G4TouchableHandle              fTouchableHandle;
  G4Navigator                    *fpNavigator;
  G4bool                         fNaviSetup;
  G4Material*                    fCsI;

};
#endif // MYPARAM_HH
