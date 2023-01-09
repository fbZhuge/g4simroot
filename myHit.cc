#include "myHit.hh"
#include "G4UnitsTable.hh"
#include <fstream>

G4ThreadLocal G4Allocator<myHit>* myHitAllocator = nullptr;

myHit::myHit(){}
myHit::~myHit(){}

G4bool myHit::operator==(const myHit& right) const {
  return ( this == &right ) ? true : false;
}

void myHit::Draw(){}

void myHit::Print() {
  G4String filename = "run.csv";
  std::ofstream logFileCsv;
  logFileCsv.open(filename, std::ios::app);
  logFileCsv
    << fChamberNb <<"," << fEdep << G4endl;
  logFileCsv.close();

  // G4cout
  //    << "trackID: "  << std::setw(7) << fTrackID
  //    << "  chamberNb: " << std::setw(7) << fChamberNb
  //    << "  Edep: "       << std::setw(7) << G4BestUnit(fEdep,"Energy")
  //    << "  Position: "  << std::setw(7) << G4BestUnit( fPos,"Length")
  //    << G4endl;
}
