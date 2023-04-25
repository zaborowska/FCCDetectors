import os
from Gaudi.Configuration import *
from GaudiKernel import SystemOfUnits as units
from GaudiKernel import PhysicalConstants as constants

from Configurables import ApplicationMgr
ApplicationMgr().EvtSel = 'NONE'
ApplicationMgr().EvtMax = 1000
ApplicationMgr().OutputLevel = INFO
ApplicationMgr().ExtSvc += ['RndmGenSvc']

from Configurables import FCCDataSvc
## Data service
podioevent = FCCDataSvc("EventDataSvc")
ApplicationMgr().ExtSvc += [podioevent]

from Configurables import MomentumRangeParticleGun
guntool = MomentumRangeParticleGun()
guntool.ThetaMin = 0.5 * constants.pi
guntool.ThetaMax = 0.5 * constants.pi
guntool.MomentumMin = 8 * units.GeV
guntool.MomentumMax = 8 * units.GeV
guntool.PdgCodes = [11]

from Configurables import GenAlg
gen = GenAlg()
gen.SignalProvider=guntool
gen.hepmc.Path = "hepmc"
ApplicationMgr().TopAlg += [gen]

from Configurables import HepMCToEDMConverter
## reads an HepMC::GenEvent from the data service and writes a collection of EDM Particles
hepmc_converter = HepMCToEDMConverter("Converter")
hepmc_converter.hepmc.Path="hepmc"
hepmc_converter.GenParticles.Path="GenParticles"
ApplicationMgr().TopAlg += [hepmc_converter]


# DD4hep geometry service
from Configurables import GeoSvc
## parse the given xml file
path_to_detectors = os.environ.get("FCCDETECTORS", "")
geoservice = GeoSvc("GeoSvc")
geoservice.detectors = [
                          os.path.join(path_to_detectors, 'Detector/DetPar04/compact/Par04_fullsim.xml'),
                       ]
ApplicationMgr().ExtSvc += [geoservice]


from Gaudi.Configuration import *
from GaudiKernel import SystemOfUnits as units
from GaudiKernel import PhysicalConstants as constants

# Geant4 service
# Configures the Geant simulation: geometry, physics list and user actions
from Configurables import SimG4Svc
# giving the names of tools will initialize the tools of that type
geantservice = SimG4Svc("SimG4Svc")
geantservice.detector =     "SimG4DD4hepDetector"
#geantservice.physicslist =  "SimG4FtfpBert"
geantservice.actions =      "SimG4FullSimActions"
from Configurables import SimG4FastSimPhysicsList, SimG4FastSimActions
physicslisttool = SimG4FastSimPhysicsList("Physics", fullphysics="SimG4FtfpBert")
geantservice.physicslist = physicslisttool
actionstool = SimG4FastSimActions("Actions")
#geantservice.actions = actionstool
from Configurables import SimG4FastSimDefineMeshRegion
regiontoolcalo = SimG4FastSimDefineMeshRegion("modelDefineMesh", volumeNames=["preECalBarrel"])
geantservice.regions=[regiontoolcalo]
ApplicationMgr().ExtSvc += [geantservice]

# Geant4 algorithm
# save tools are set up alongside the geoservice
from Configurables import SimG4Alg
geantsim = SimG4Alg("SimG4Alg")
from Configurables import SimG4SaveTrackerHits
from Configurables import SimG4PrimariesFromEdmTool
geantsim.eventProvider = SimG4PrimariesFromEdmTool("EdmConverter")
geantsim.eventProvider.GenParticles.Path = "GenParticles"
ApplicationMgr().TopAlg += [geantsim]

from Configurables import SimG4SaveCalHits
saveEcalBarreltool = SimG4SaveCalHits("saveEcalBarrelHits")
saveEcalBarreltool.readoutNames = ["ShowerCylinderMesh"]
saveEcalBarreltool.CaloHits.Path = "hits_EcalBarrel"
SimG4Alg("SimG4Alg").outputs += [saveEcalBarreltool]

from Configurables import SimG4FastSimMeshHistograms
hists = SimG4FastSimMeshHistograms("validaitonHistograms")
hists.MCparticles.Path = "GenParticles"
hists.Hits.Path = "hits_EcalBarrel"
hists.readoutName = "ShowerCylinderMesh"
hists.meshSizeRho = 2.325 * units.mm
hists.meshSizeZ = 3.4 * units.mm
hists.OutputLevel = INFO
THistSvc().Output = ["sim DATAFILE='out_hist_fullsim_par04_8GeV_1000events.root' TYP='ROOT' OPT='RECREATE'"]
THistSvc().PrintAll = True
THistSvc().AutoSave = True
THistSvc().AutoFlush = True
THistSvc().OutputLevel = DEBUG
ApplicationMgr().TopAlg += [hists]

# PODIO algorithm
from Configurables import PodioOutput
out = PodioOutput("out")
out.filename = "out_geant_fullsim_par04_8GeV_1000events.root"
out.OutputLevel = DEBUG
out.outputCommands = ["keep *"]
ApplicationMgr().TopAlg += [out]

export_fname = "TestBox.gdml"
# check if file exists and delete it:
if os.path.isfile(export_fname):
    os.remove(export_fname)
from Configurables import GeoToGdmlDumpSvc
geodumpservice = GeoToGdmlDumpSvc("GeoDump", gdml=export_fname)
ApplicationMgr().ExtSvc += [geodumpservice]
