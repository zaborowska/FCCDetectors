#include "DetSensitive/DynamicMeshCalorimeterSD.h"

// FCCSW
#include "DetCommon/DetUtils.h"
#include "DetCommon/Geant4CaloHit.h"

// DD4hep
#include "DDG4/Defs.h"
#include "DDG4/Geant4Mapping.h"
#include "DDG4/Geant4VolumeManager.h"

// CLHEP
#include "CLHEP/Vector/ThreeVector.h"

// Geant4
#include "G4SDManager.hh"

namespace det {
DynamicMeshCalorimeterSD::DynamicMeshCalorimeterSD(const std::string& aDetectorName,
                                         const std::string& aReadoutName,
                                         const dd4hep::Segmentation& aSeg)
    : G4VSensitiveDetector(aDetectorName), m_calorimeterCollection(nullptr), m_seg(aSeg) {
  // name of the collection of hits is determined byt the readout name (from XML)
  collectionName.insert(aReadoutName);
}

DynamicMeshCalorimeterSD::~DynamicMeshCalorimeterSD() {}

void DynamicMeshCalorimeterSD::Initialize(G4HCofThisEvent* aHitsCollections) {
  // create a collection of hits and add it to G4HCofThisEvent
  // deleted in ~G4Event
  m_calorimeterCollection = new G4THitsCollection<k4::Geant4CaloHit>(SensitiveDetectorName, collectionName[0]);
  aHitsCollections->AddHitsCollection(G4SDManager::GetSDMpointer()->GetCollectionID(m_calorimeterCollection),
                                      m_calorimeterCollection);

  G4int sizePhi = 4;
  G4int sizeR = 5;
  G4int sizeZ = 3;
  // fill calorimeter hits with zero energy deposition
  for (G4int iHit = 0; iHit < sizePhi * sizeR * sizeZ; iHit++) {
    k4::Geant4CaloHit* hit = new k4::Geant4CaloHit(0, 0, 0, 0);
    m_calorimeterCollection->insert(hit);
  }
  G4int iCell = 0;
  for(G4int iphi = 0; iphi < sizePhi; iphi++)
    for(G4int irho = 0; irho < sizeR; irho++)
      for(G4int iz = 0; iz < sizeZ; iz++)
        {
          iCell = sizePhi * sizeR * iz + sizePhi * ir + iphi;
          G4cout<<"\tphi = " << iphi <<"\tr = " << ir << "\tz = " << iz << "\tCELL ID = " << iCell << G4endl;
        }
  // reset entrance position
  fEntrancePosition.set(-1, -1, -1);
  fEntranceDirection.set(-1, -1, -1);
}

bool DynamicMeshCalorimeterSD::ProcessHits(G4Step* aStep, G4TouchableHistory*) {
  // check if energy was deposited
  G4double edep = aStep->GetTotalEnergyDeposit();
  if (edep == 0.) return false;
/*
  // as in dd4hep::sim::Geant4GenericSD<Calorimeter>
  const G4Track* track = aStep->GetTrack();
  auto hit = new k4::Geant4CaloHit(
      track->GetTrackID(), track->GetDefinition()->GetPDGEncoding(), edep, track->GetGlobalTime());

  hit->energyDeposit += edep;

*/
  return true;
}
}
