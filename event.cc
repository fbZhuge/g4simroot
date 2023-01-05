#include "event.hh"
#include "G4UnitsTable.hh"


MyEventAction::MyEventAction(MyRunAction*)
{
}

MyEventAction::~MyEventAction(){}

void MyEventAction::BeginOfEventAction(const G4Event*)
{
}

void MyEventAction::EndOfEventAction(const G4Event* event)
{
  // get number of stored trajectories

  G4TrajectoryContainer* trajectoryContainer = event->GetTrajectoryContainer();
  G4int numberOfTrajectories = 0;
  if (trajectoryContainer) numberOfTrajectories = trajectoryContainer->entries();

  // periodic printing

  G4int eventID = event->GetEventID();
  G4cout << ">>> Event: " << eventID  << G4endl;
  if ( trajectoryContainer ) {
    G4cout << "    " << numberOfTrajectories
           << " trajectories stored in this event." << G4endl;
  }

  // G4VHitsCollection* hc = event->GetHCofThisEvent()->GetHC(0);
  // G4cout << "    "
  //        << hc->GetSize() << " hits stored in this event" << G4endl;
}





// for(G4int i=0; i<10; i++){
//   for(G4int j=0; j<10; j++){
//     for(G4int k=0; k<10; k++){
//       G4cout<< "fEnergyVoxel[i][j][k]" << MySensitiveDetector::fEnergyVoxel[i][j][k] << G4endl;
//     }
//   }
// }
