#include "detector.hh"

MySensitiveDetector::MySensitiveDetector(const G4String& name,
                                         const G4String& hitsCollectionName)
  : G4VSensitiveDetector(name)
{
  // collectionName is a protected member of G4VSensitiveDetector class, it is vector of G4String
  collectionName.insert(hitsCollectionName);
}

MySensitiveDetector::~MySensitiveDetector(){}

void MySensitiveDetector::Initialize(G4HCofThisEvent* hce)
{
  // Create hits collection
  // SensitiveDetectorName is a protected memeber of G4VSensetiveDetector
  fHitsCollection = new myHitsCollection(SensitiveDetectorName, collectionName[0]);

  // Add this collection in hce

  // G4int hcID = G4SDManager::GetSDMpointer()->GetCollectionID(collectionName[0]);
  // G4cout << "hcID = "<< hcID << G4endl;
  // hce->AddHitsCollection(hcID, fHitsCollection);
}

G4bool MySensitiveDetector::ProcessHits(G4Step *aStep, G4TouchableHistory*)
{
  G4double edep = aStep->GetTotalEnergyDeposit();
  if (edep==0.) return false;
  G4int Chamber_Number = aStep->GetPreStepPoint()->GetTouchableHandle()->GetCopyNumber();
  G4int Track_ID = aStep->GetTrack()->GetTrackID();

  myHit* newHit = new myHit();

  G4int index_x=Chamber_Number%100;
  G4int index_y=((Chamber_Number-index_x)/100)%100;
  G4int index_z=(Chamber_Number-index_x-(100*index_y))/10000;

  // G4cout << "Chamber_Number = " << Chamber_Number << G4endl;
  // G4cout << "  index_x = " << index_x << G4endl;
  // G4cout << "  index_y = " << index_y << G4endl;
  // G4cout << "  index_z = " << index_z << G4endl;

  // Set_Energy_Voxel(index_x, index_y, index_z, edep);

  newHit->SetTrackID(Track_ID);
  newHit->SetChamberNb(Chamber_Number);
  newHit->SetEdep(edep);
  newHit->SetPos (aStep->GetPostStepPoint()->GetPosition());

  // fHitsCollection->insert(newHit);

  // newHit->Print();
  return true;
}

void MySensitiveDetector::EndOfEvent(G4HCofThisEvent*)
{
  // Create_Profiles();
  // auto analysisManager = G4AnalysisManager::Instance();

  // for(G4int i=0; i<10; i++){
  //   for(G4int j=0; j<10; j++){
  //     for(G4int k=0; k<10; k++){
  //       G4cout<< "fEnergyVoxel[i][j][k]" << fEnergyVoxel[i][j][k] << G4endl;
  //     }
  //   }
  // }
  // analysisManager->FillNtupleDColumn(0, fY_Profile[0]);
  // analysisManager->FillNtupleDColumn(1, fY_Profile[1]);
  // analysisManager->FillNtupleDColumn(2, fY_Profile[2]);
  // analysisManager->FillNtupleDColumn(3, fY_Profile[3]);
  // analysisManager->FillNtupleDColumn(4, fY_Profile[4]);
  // analysisManager->FillNtupleDColumn(5, fY_Profile[5]);
  // analysisManager->FillNtupleDColumn(6, fY_Profile[6]);
  // analysisManager->FillNtupleDColumn(7, fY_Profile[7]);
  // analysisManager->FillNtupleDColumn(8, fY_Profile[8]);
  // analysisManager->FillNtupleDColumn(9, fY_Profile[9]);

  // for(G4int i=0; i<10; i++){
  //   for(G4int j=0; j<10; j++){
  //     for(G4int k=0; k<10; k++){
  //       analysisManager->FillNtupleDColumn(k+10*j+100*i,fEnergyVoxel[i][j][k]);
  //     }
  //   }
  // }
  // analysisManager->AddNtupleRow();

  // G4cout<< "fEnergy_dist[3] = " << fEnergy_dist[3];
  // G4int nofHits = fHitsCollection->entries();
  // G4cout << G4endl
  //        << "-------->Hits Collection: in this event they are " << nofHits
  //        << " hits in the tracker chambers: " << G4endl;
  // for ( G4int i=0; i<nofHits; i++ ) (*fHitsCollection)[i]->Print();
}




// void MySensitiveDetector::Set_Energy(G4int index, G4double energy){
//   fEnergy_dist[index] += energy;
// }

// void MySensitiveDetector::Set_Energy_Voxel(G4int i, G4int j, G4int k, G4double energy){
//   fEnergyVoxel[i][j][k]+=energy;
// }

// void MySensitiveDetector::Create_Profiles(){
//   for(G4int i=0; i<10; i++){
//     for(G4int j=0; j<10; j++){
//       for(G4int k=0; k<10; k++){
//         fX_Profile[i]+=fEnergyVoxel[i][j][k];
//         fY_Profile[j]+=fEnergyVoxel[i][j][k];
//         fZ_Profile[k]+=fEnergyVoxel[i][j][k];
//       }
//     }
//     G4cout << "fX_Profile: "<<fX_Profile[i]<<G4endl;
//   }
// }
