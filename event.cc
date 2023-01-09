#include "event.hh"
#include "G4UnitsTable.hh"

MyEventAction::MyEventAction(MyRunAction*){}
MyEventAction::~MyEventAction(){}
void MyEventAction::BeginOfEventAction(const G4Event*){}

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
}
