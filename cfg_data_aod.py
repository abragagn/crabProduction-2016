import FWCore.ParameterSet.Config as cms
#from PhysicsTools.PatAlgos.tools.helpers import getPatAlgosToolsTask

process = cms.Process("bphAnalysis")

#patAlgosToolsTask = getPatAlgosToolsTask(process)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(20) )
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.options.allowUnscheduled = cms.untracked.bool(True)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/lustre/cmswork/cmsdata/ronchese/store/data/Run2016H/Charmonium/AOD/07Aug17-v1/10000/0003E4A7-F19A-E711-963D-1866DAEA8178.root')
#    fileNames = cms.untracked.vstring('file:/lustre/cmswork/cmsdata/ronchese/store/data/Run2016H/Charmonium/AOD/18Apr2017-v1/00000/0004D8F8-6E50-E711-BA0F-3417EBE6463F.root')
#    fileNames = cms.untracked.vstring('file:/lustre/cmswork/cmsdata/ronchese/store/data/Run2017C/Charmonium/AOD/PromptReco-v2/000/300/079/00000/1C712689-2177-E711-944B-02163E01472F.root')
)

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '92X_dataRun2_Prompt_v2', '')
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

process.load('PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff')
#patAlgosToolsTask.add(process.patCandidatesTask)
process.load('PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff')
#patAlgosToolsTask.add(process.selectedPatCandidatesTask)
process.load('PhysicsTools.PatAlgos.cleaningLayer1.cleanPatCandidates_cff')
#patAlgosToolsTask.add(process.cleanPatCandidatesTask)

### add trigger information to the configuration
from PhysicsTools.PatAlgos.tools.trigTools import *
switchOnTrigger( process, None, None, None, None, '' )

process.selectedPatMuons.cut = cms.string('muonID(\"TMOneStationTight\")'
                    ' && abs(innerTrack.dxy) < 0.3'
                    ' && abs(innerTrack.dz)  < 20.'
                    ' && innerTrack.hitPattern.trackerLayersWithMeasurement > 5'
                    ' && innerTrack.hitPattern.pixelLayersWithMeasurement > 0'
                    ' && innerTrack.quality(\"highPurity\")'
                    )

#make patTracks
from PhysicsTools.PatAlgos.tools.trackTools import makeTrackCandidates
makeTrackCandidates(process,
                    label        = 'TrackCands',                  # output collection
                    tracks       = cms.InputTag('generalTracks'), # input track collection
                    particleType = 'pi+',                         # particle type (for assigning a mass)
                    preselection = 'pt > 0.7',                    # preselection cut on candidates
                    selection    = 'pt > 0.7',                    # selection on PAT Layer 1 objects
                    isolation    = {},                            # isolations to use (set to {} for None)
                    isoDeposits  = [],
                    mcAs         = None                           # replicate MC match as the one used for Muons
)
process.patTrackCands.embedTrack = True

# reduce MC genParticles a la miniAOD
#process.load('PhysicsTools.PatAlgos.slimming.genParticles_cff')
#process.packedGenParticles.inputVertices = cms.InputTag('offlinePrimaryVertices')

from PhysicsTools.PatAlgos.tools.coreTools import runOnData
runOnData( process, outputModules = [] )


### vtxTagInfo
#
#process.load('RecoBTag/SoftLepton/softLepton_cff')
#
##process.load('RecoBTag/SoftLepton/softPFMuonTagInfos_cfi')
##process.load('RecoBTag/SoftLepton/softPFElectronTagInfos_cfi')
#
#process.load('RecoBTag/SecondaryVertex/pfInclusiveSecondaryVertexFinderTagInfos_cfi')
#process.load('RecoBTag/ImpactParameter/pfImpactParameterTagInfos_cfi')
#
##process.load('RecoBTag/SecondaryVertex/secondaryVertexTagInfos_cfi')
#
#process.softPFMuonsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
#process.softPFMuonsTagInfos.jets = cms.InputTag("selectedPatJets")
#process.softPFMuonsTagInfos.muons = cms.InputTag("selectedPatMuons")
#
#process.softPFElectronsTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
#process.softPFElectronsTagInfos.jets = cms.InputTag("selectedPatJets")
#process.softPFElectronsTagInfos.electrons = cms.InputTag("selectedPatElectrons")
#
#process.pfImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
#process.pfImpactParameterTagInfos.jets = cms.InputTag("selectedPatJets")
#process.pfImpactParameterTagInfos.candidates = cms.InputTag("particleFlow::RECO")
#
#process.tagInfoProd = cms.Sequence(
#    process.softPFMuonsTagInfos
#    + process.softPFElectronsTagInfos
#    + process.pfImpactParameterTagInfos
#    * process.pfSecondaryVertexTagInfos
#)
#
### vtxTagInfo end


process.pdAnalyzer = cms.EDAnalyzer('PDNtuplizer',

    ## optional
    eventList = cms.string('evtlist'),
    verbose = cms.untracked.string('f'),
    evStamp = cms.untracked.string('f'),

    ## mandatory
    ## ntuple file name: empty string to drop ntuple filling
    ntuName = cms.untracked.string('ntu.root'),
    ## histogram file name
    histName = cms.untracked.string('his.root'),

    labelTrigResults  = cms.string('TriggerResults::HLT'), 
    labelTrigEvent    = cms.string('patTriggerEvent'),
    labelBeamSpot     = cms.string('offlineBeamSpot'),
    labelMets         = cms.string('patMETs'),
    labelMuons        = cms.string('selectedPatMuons'),
    labelElectrons    = cms.string('selectedPatElectrons'),
#    labelTaus         = cms.string('selectedPatTaus'),
    labelTaus         = cms.string(''),

    labelJets         = cms.string('selectedPatJets'),
    labelPFCandidates = cms.string('particleFlow::RECO'),

    labelGeneralTracks = cms.string('generalTracks'),
    labelPVertices    = cms.string('offlinePrimaryVertices'),
    labelSVertices    = cms.string(''),
#    labelSVertices    = cms.string('pfSecondaryVertexTagInfos'),
    labelSVTagInfo    = cms.string(''),
    labelPUInfo       = cms.string(''),
    labelGen          = cms.string(''),
    labelGPJ          = cms.string(''),

    labelCSV          = cms.string('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
    labelTCHE         = cms.string('trackCountingHighEffBJetTags'),

    vertReco = cms.vstring('svtBuJPsiK','svtBdJPsiKx','svtBsJPsiPhi'),

    acceptNewTrigPaths = cms.string('f'),
    write_hltlist = cms.string('f'),

    selectAssociatedPF = cms.string('f'),
    selectAssociatedTk = cms.string('f'),
    recoverMuonTracks = cms.string('t'),
    writeAllPrimaryVertices = cms.string('t'),

    jetPtMin  = cms.double(  5.0 ),
    jetEtaMax = cms.double(  2.5 ),
    trkDzMax  = cms.double(  0.8 ),
    trkPtMin  = cms.double(  0.5 ),
    trkEtaMax = cms.double(  3.0 ),
    dRmatchHLT = cms.double( 0.5 ),
    dPmatchHLT = cms.double( 0.5 ),


    savedTriggerPaths = cms.vstring(
        '*'
    ),

    ## trigger objects to save on ntuple:
    savedTriggerObjects = cms.vstring(
        'hltJet',
        'hltMuon',
        'hltTrack'
    ),

    ## jet user info to save on ntuple:
    savedJetInfo = cms.vstring(
#        'puBeta*'
    )

)

#process.evNumFilter = cms.EDFilter('EvNumFilter',
#    eventList = cms.string('evList')
#)

#############################################################
#### PATH definition
#############################################################
# Let it run
process.p = cms.Path(
#    process.evNumFilter *
#    process.tagInfoProd *
    process.pdAnalyzer
#,
#    patAlgosToolsTask
)

#process.out = cms.OutputModule("PoolOutputModule",
#    outputCommands = cms.untracked.vstring('keep *_*_*_HLT',
#                                           'keep *_*_*_RECO',
#                                           'keep *_*_*_PAT',
#                                           'drop *_*_*_pdSelect'),
##                                           'drop *_puJetId_*_*',
##  output file name:
#    fileName = cms.untracked.string('selPAT.root'),   
#    SelectEvents = cms.untracked.PSet(
#        SelectEvents = cms.vstring('p')
#    )
#)
#
#process.e = cms.EndPath(process.out)

