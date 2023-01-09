#include "detector.hh"

MySensitiveDetector::MySensitiveDetector(const G4String& name, const G4String& hitsCollectionName) : G4VSensitiveDetector(name)
{
  // collectionName is a protected member of G4VSensitiveDetector class, it is vector of G4String
  collectionName.insert(hitsCollectionName);
}

MySensitiveDetector::~MySensitiveDetector(){}
void MySensitiveDetector::Initialize(G4HCofThisEvent* hce) {}

G4bool MySensitiveDetector::ProcessHits(G4Step *aStep, G4TouchableHistory*)
{
  G4double edep = aStep->GetTotalEnergyDeposit();
  if (edep==0.) return false;
  G4int Chamber_Number = aStep->GetPreStepPoint()->GetTouchableHandle()->GetCopyNumber();
  G4int Track_ID = aStep->GetTrack()->GetTrackID();

  myHit *newHit = new myHit();

  // G4int index_x=Chamber_Number%100;
  // G4int index_y=((Chamber_Number-index_x)/100)%100;
  // G4int index_z=(Chamber_Number-index_x-(100*index_y))/10000;

  newHit->SetTrackID(Track_ID);
  newHit->SetChamberNb(Chamber_Number);
  newHit->SetEdep(edep);
  newHit->SetPos (aStep->GetPostStepPoint()->GetPosition());

  newHit->Print();
  return true;
}

void MySensitiveDetector::EndOfEvent(G4HCofThisEvent*) {}
