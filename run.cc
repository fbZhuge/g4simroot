#include "run.hh"

MyRunAction::MyRunAction(){
  // auto analysisManager = G4AnalysisManager::Instance();
  // G4int verboseLevel=1; // [0..4]
  // analysisManager->SetVerboseLevel(verboseLevel);

  // analysisManager->CreateNtuple("Energy_Deposits","Edep");

  // analysisManager->FinishNtuple(1);
}

MyRunAction::~MyRunAction(){}

void MyRunAction::BeginOfRunAction(const G4Run* run)
{
  // auto analysisManager = G4AnalysisManager::Instance();

  // G4int runID = run->GetRunID();
  // std::stringstream strRunID;
  // strRunID << runID;

  // G4String filename = "myRootFile"+strRunID.str()+".root";
  // analysisManager->OpenFile(filename);
}

void MyRunAction::EndOfRunAction(const G4Run*)
{
  // auto analysisManager = G4AnalysisManager::Instance();
  // analysisManager->Write();
  // analysisManager->CloseFile();
}
