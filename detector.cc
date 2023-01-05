#include "detector.hh"

MySensitiveDetector::MySensitiveDetector(const G4String& name,
                                         const G4String& hitsCollectionName)
  : G4VSensitiveDetector(name)
{
  // collectionName is a protected member of G4VSensitiveDetector class, it is vector of G4String
  collectionName.insert(hitsCollectionName);
}

MySensitiveDetector::~MySensitiveDetector(){}

void MySensitiveDetector::Initialize(G4HCofThisEvent *hitCollectionOfThisEvent)
{
  // Create hits collection
  // SensitiveDetectorName is a protected memeber of G4VSensetiveDetector
  // myHitsCollection is a typedef to G4THitsCollection<myHit>
  fHitsCollection = new myHitsCollection(SensitiveDetectorName, collectionName[0]);

  // Add this collection in hce
  G4int hcID = G4SDManager::GetSDMpointer()->GetCollectionID(collectionName[0]);
  // G4cout << "hcID = "<< hcID << G4endl;
  hitCollectionOfThisEvent->AddHitsCollection(hcID, fHitsCollection);
}

G4bool MySensitiveDetector::ProcessHits(G4Step *aStep, G4TouchableHistory*)
{
  G4double edep = aStep->GetTotalEnergyDeposit();
  if (edep==0.) return false;
  G4int Chamber_Number = aStep->GetPreStepPoint()->GetTouchableHandle()->GetCopyNumber();
  G4int Track_ID = aStep->GetTrack()->GetTrackID();

  myHit *newHit = new myHit();
  newHit->SetTrackID(Track_ID);
  newHit->SetChamberNb(Chamber_Number);
  newHit->SetEdep(edep);
  newHit->SetPos(aStep->GetPostStepPoint()->GetPosition());

  // this line induces a SegFault!
  if (newHit) G4int hitCollectionSize = fHitsCollection->insert(newHit);

  // newHit->Print();
  return true;
}

void MySensitiveDetector::EndOfEvent(G4HCofThisEvent*)
{
  G4int nofHits = fHitsCollection->entries();
  G4cout << G4endl
         << "-------->Hits Collection: in this event they are " << nofHits
         << " hits in the tracker chambers: " << G4endl;
  for (G4int i=0; i<nofHits; i++) (*fHitsCollection)[i]->Print();
}
