#ifndef DETECTOR_HH
#define DETECTOR_HH

#include "G4VSensitiveDetector.hh"
#include "G4AnalysisManager.hh"
#include "G4RunManager.hh"
#include "G4SDManager.hh"
#include "myHit.hh"
#include <vector>

class MySensitiveDetector : public G4VSensitiveDetector{

public:
  MySensitiveDetector(const G4String& name,
                      const G4String& hitsCollectionName);
  ~MySensitiveDetector() override;

  // methods from base class
  void   Initialize(G4HCofThisEvent* hitCollection) override;
  G4bool ProcessHits(G4Step* step, G4TouchableHistory* history) override;
  void   EndOfEvent(G4HCofThisEvent* hitCollection) override;

  // my custom methods
  // void Set_Energy_Voxel(G4int i, G4int j, G4int k, G4double energy);
  // void Create_Profiles();

private:
  myHitsCollection* fHitsCollection = nullptr;

  // G4double fEnergyVoxel[10][10][10]={0};
  // G4double fX_Profile[10]={0};
  // G4double fY_Profile[10]={0};
  // G4double fZ_Profile[10]={0};
};
#endif
