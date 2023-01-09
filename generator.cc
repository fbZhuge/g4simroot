#include "generator.hh"

MyPrimaryGenerator::MyPrimaryGenerator()
{
  fParticleGun = new G4ParticleGun(10);
}

MyPrimaryGenerator::~MyPrimaryGenerator(){
  delete fParticleGun;
}

void MyPrimaryGenerator::GeneratePrimaries(G4Event *anEvent)
{
  G4ParticleTable *particleTable = G4ParticleTable::GetParticleTable();
  // G4String particleName = "proton";
  G4String particleName = "e-";

  G4ParticleDefinition *particle = particleTable->FindParticle(particleName);
  G4ThreeVector pos(0.,0.,-10);
  G4ThreeVector mom(0.,0.,1.);

  fParticleGun->SetParticleMomentumDirection(mom);
  fParticleGun->SetParticleMomentum(3.0*GeV);
  fParticleGun->SetParticleDefinition(particle);
  fParticleGun->SetParticlePosition(pos);

  fParticleGun->GeneratePrimaryVertex(anEvent);
}
