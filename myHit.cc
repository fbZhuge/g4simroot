#include "myHit.hh"
#include "G4UnitsTable.hh"
#include <fstream>

G4ThreadLocal G4Allocator<myHit> *myHitAllocator = nullptr;

myHit::myHit(){}
myHit::~myHit(){}

G4bool myHit::operator==(const myHit& right) const
{
  return ( this == &right ) ? true : false;
}

void myHit::Draw(){}

void myHit::Print()
{
  G4cout
    // << "trackID: "  << std::setw(7) << fTrackID
    << "  chamberNb: " << std::setw(7) << fChamberNb
    << "  Edep: "       << std::setw(7) << G4BestUnit(fEdep,"Energy")
    //    << "  Position: "  << std::setw(7) << G4BestUnit( fPos,"Length")
    << G4endl;
}











// std::ofstream logFileCsv;
// logFileCsv.open("hits_csv.csv", std::ios::app);
// logFileCsv
//   << fChamberNb <<"," << fEdep << G4endl;
// logFileCsv.close();

// std::ofstream logFile;
// logFile.open("hits_log", std::ios::app);
// logFile
//   << "trackID: "  << std::setw(7) << fTrackID
//   << "chamberNb: " << std::setw(7) << fChamberNb
//   << "Edep: "       << std::setw(7) << G4BestUnit(fEdep,"Energy")
//   << "Position: " << std::setw(7) << G4BestUnit( fPos,"Length")
//   << G4endl;
// logFile.close();
