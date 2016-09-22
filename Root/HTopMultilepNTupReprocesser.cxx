// package include(s):
#include <HTopMultilepAnalysis/HTopMultilepNTupReprocesser.h>
#include "HTopMultilepAnalysis/tools/HTopReturnCheck.h"

// ASG status code check
#include <AsgTools/MessageCheck.h>

// ROOT include(s)
#include "TObjArray.h"

// C++ include(s)
#include <iomanip>
#include <memory>

using namespace NTupReprocesser;

// this is needed to distribute the algorithm to the workers
ClassImp(HTopMultilepNTupReprocesser)

HTopMultilepNTupReprocesser :: HTopMultilepNTupReprocesser(std::string className) :
    Algorithm(className),
    m_inputNTuple(nullptr),
    m_outputNTuple(nullptr),
    m_isQMisIDBranchIn(false),
    m_isMMBranchIn(false),
    m_doQMisIDWeighting(false),
    m_doMMWeighting(false)
{
  // Here you put any code for the base initialization of variables,
  // e.g. initialize all pointers to 0.  Note that you should only put
  // the most basic initialization here, since this method will be
  // called on both the submission and the worker node.  Most of your
  // initialization code will go into histInitialize() and
  // initialize().

  Info("HTopMultilepNTupReprocesser()", "Calling constructor");

  m_inputBranches        = "";

  m_outputNTupName       = "physics";
  m_outputNTupStreamName = "output";

  m_weightToCalc         = "";

  m_QMisIDRates_dir            = "";
  m_QMisIDRates_Filename_T     = "";
  m_QMisIDRates_Filename_AntiT = "";
  m_useTAntiTRates             = false;

  m_REFF_dir                = "";
  m_FEFF_dir                = "";
  m_EFF_YES_TM_dir          = "";
  m_EFF_NO_TM_dir           = "";
  m_Efficiency_Filename     = "";
  m_doMMClosure             = false;
  m_useEtaParametrisation   = false;
  m_useTrigMatchingInfo     = false;
  m_useScaledFakeEfficiency = false;
  m_useTEfficiency          = false;
  
  m_systematics_list        = "Stat";

}



EL::StatusCode HTopMultilepNTupReprocesser :: setupJob (EL::Job& job)
{
  // Here you put code that sets up the job on the submission object
  // so that it is ready to work with your algorithm, e.g. you can
  // request the D3PDReader service or add output files.  Any code you
  // put here could instead also go into the submission script.  The
  // sole advantage of putting it here is that it gets automatically
  // activated/deactivated when you add/remove the algorithm from your
  // job, which may or may not be of value to you.

  //ANA_CHECK_SET_TYPE (EL::StatusCode); // set type of return code you are expecting (add to top of each function once)

  Info("setupJob()", "Calling setupJob");

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode HTopMultilepNTupReprocesser :: histInitialize ()
{
  // Here you do everything that needs to be done at the very
  // beginning on each worker node, e.g. create histograms and output
  // trees.  This method gets called before any input files are
  // connected.

  //ANA_CHECK_SET_TYPE (EL::StatusCode);

  Info("histInitialize()", "Calling histInitialize");

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode HTopMultilepNTupReprocesser :: fileExecute ()
{
  // Here you do everything that needs to be done exactly once for every
  // single file, e.g. collect a list of all lumi-blocks processed

  //ANA_CHECK_SET_TYPE (EL::StatusCode);

  Info("fileExecute()", "Calling fileExecute");

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode HTopMultilepNTupReprocesser :: changeInput (bool firstFile)
{
  // Here you do everything you need to do when we change input files,
  // e.g. resetting branch addresses on trees.  If you are using
  // D3PDReader or a similar service this method is not needed.

  ANA_CHECK_SET_TYPE (EL::StatusCode);

  firstFile = firstFile;

  Info("changeInput()", "Calling changeInput. Now reading file : %s", wk()->inputFile()->GetName() );

  // Get the pointer to the main input TTree
  //
  m_inputNTuple = wk()->tree();

  // Check content of input tree
  //
  TObjArray* branches = m_inputNTuple->GetListOfBranches();
  int nbranches = branches->GetEntriesFast();
  for ( int idx(0); idx < nbranches; ++idx ) {
      std::string this_branch(branches->At(idx)->GetName());
      if ( this_branch.find("QMisIDWeight") != std::string::npos ) {
	  m_isQMisIDBranchIn = true;
	  break;
      }
  }
  for ( int idx(0); idx < nbranches; ++idx ) {
      std::string this_branch(branches->At(idx)->GetName());
      if ( this_branch.find("MMWeight") != std::string::npos ) {
	  m_isMMBranchIn = true;
	  break;
      }
  }

  ANA_CHECK( this->enableSelectedBranches() );

  // Connect the branches of the input tree to the algorithm members
  //
  m_inputNTuple->SetBranchAddress ("EventNumber",   			      &m_EventNumber);
  m_inputNTuple->SetBranchAddress ("RunNumber",   			      &m_RunNumber);
  m_inputNTuple->SetBranchAddress ("mc_channel_number",                       &m_mc_channel_number);
  m_inputNTuple->SetBranchAddress ("isSS01",                                  &m_isSS01);
  m_inputNTuple->SetBranchAddress ("dilep_type",  			      &m_dilep_type);
  m_inputNTuple->SetBranchAddress ("trilep_type",  			      &m_trilep_type);
  m_inputNTuple->SetBranchAddress ("is_T_T",				      &m_is_T_T);
  m_inputNTuple->SetBranchAddress ("is_T_AntiT",			      &m_is_T_AntiT);
  m_inputNTuple->SetBranchAddress ("is_AntiT_T",			      &m_is_AntiT_T);
  m_inputNTuple->SetBranchAddress ("is_AntiT_AntiT",			      &m_is_AntiT_AntiT);

  m_inputNTuple->SetBranchAddress ("lep_ID_0",   			      &m_lep_ID_0);
  m_inputNTuple->SetBranchAddress ("lep_Pt_0",  			      &m_lep_Pt_0);
  m_inputNTuple->SetBranchAddress ("lep_E_0",   			      &m_lep_E_0);
  m_inputNTuple->SetBranchAddress ("lep_Eta_0",  			      &m_lep_Eta_0);
  m_inputNTuple->SetBranchAddress ("lep_Phi_0",   			      &m_lep_Phi_0);
  m_inputNTuple->SetBranchAddress ("lep_EtaBE2_0",   			      &m_lep_EtaBE2_0);
  m_inputNTuple->SetBranchAddress ("lep_isTightSelected_0",   		      &m_lep_isTightSelected_0);
  m_inputNTuple->SetBranchAddress ("lep_isTrigMatch_0",   		      &m_lep_isTrigMatch_0);

  m_inputNTuple->SetBranchAddress ("lep_ID_1",   			      &m_lep_ID_1);
  m_inputNTuple->SetBranchAddress ("lep_Pt_1",  			      &m_lep_Pt_1);
  m_inputNTuple->SetBranchAddress ("lep_E_1",   			      &m_lep_E_1);
  m_inputNTuple->SetBranchAddress ("lep_Eta_1",  			      &m_lep_Eta_1);
  m_inputNTuple->SetBranchAddress ("lep_Phi_1",   			      &m_lep_Phi_1);
  m_inputNTuple->SetBranchAddress ("lep_EtaBE2_1",   			      &m_lep_EtaBE2_1);
  m_inputNTuple->SetBranchAddress ("lep_isTightSelected_1",   		      &m_lep_isTightSelected_1);
  m_inputNTuple->SetBranchAddress ("lep_isTrigMatch_1",   		      &m_lep_isTrigMatch_1);

  if ( m_isQMisIDBranchIn ) {
      m_inputNTuple->SetBranchAddress ("QMisIDWeight",     &m_QMisIDWeight_in);
      m_inputNTuple->SetBranchAddress ("QMisIDWeight_up",  &m_QMisIDWeight_UP_in);
      m_inputNTuple->SetBranchAddress ("QMisIDWeight_dn",  &m_QMisIDWeight_DN_in);
  }
  if ( m_isMMBranchIn ) {
      m_inputNTuple->SetBranchAddress ("MMWeight",           &m_MMWeight_in);
      m_inputNTuple->SetBranchAddress ("MMWeight_lep0_r_up", &m_weight_MM_lep0_R_stat_UP_in);
      m_inputNTuple->SetBranchAddress ("MMWeight_lep0_r_dn", &m_weight_MM_lep0_R_stat_DN_in);
      m_inputNTuple->SetBranchAddress ("MMWeight_lep1_r_up", &m_weight_MM_lep1_R_stat_UP_in);
      m_inputNTuple->SetBranchAddress ("MMWeight_lep1_r_dn", &m_weight_MM_lep1_R_stat_DN_in);
      m_inputNTuple->SetBranchAddress ("MMWeight_lep0_f_up", &m_weight_MM_lep0_F_stat_UP_in);
      m_inputNTuple->SetBranchAddress ("MMWeight_lep0_f_dn", &m_weight_MM_lep0_F_stat_DN_in);
      m_inputNTuple->SetBranchAddress ("MMWeight_lep1_f_up", &m_weight_MM_lep1_F_stat_UP_in);
      m_inputNTuple->SetBranchAddress ("MMWeight_lep1_f_dn", &m_weight_MM_lep1_F_stat_DN_in);
  }

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode  HTopMultilepNTupReprocesser :: tokenize ( char separator, std::vector<std::string>& vec_tokens, const std::string& list ) {

  std::string token;
  std::istringstream ss( list );
  while ( std::getline(ss, token, separator) ) { vec_tokens.push_back(token); }

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode HTopMultilepNTupReprocesser :: initialize ()
{
  // Here you do everything that you need to do after the first input
  // file has been connected and before the first event is processed,
  // e.g. create additional histograms based on which variables are
  // available in the input files.  You can also create all of your
  // histograms and trees in here, but be aware that this method
  // doesn't get called if no events are processed.  So any objects
  // you create here won't be available in the output if you have no
  // input events.

  ANA_CHECK_SET_TYPE (EL::StatusCode);

  Info("initialize()", "Initialising HTopMultilepNTupReprocesser...");

  m_outputNTuple = EL::getNTupleSvc (wk(), m_outputNTupStreamName);

  // Parse input weight list, split by comma, and put into a vector
  //
  std::vector<std::string> weights;
  ANA_CHECK( this->tokenize( ',', weights, m_weightToCalc ) );
    
  if ( std::find( weights.begin(), weights.end(), "QMisID" ) != weights.end() ) { m_doQMisIDWeighting = true; }
  if ( std::find( weights.begin(), weights.end(), "MM" ) != weights.end() )	{ m_doMMWeighting = true; }

  // Set new branches for output TTree
  //
  if ( m_doQMisIDWeighting ) {
      m_outputNTuple->tree()->Branch("QMisIDWeight",     &m_QMisIDWeight_out,    "QMisIDWeight/F");
      m_outputNTuple->tree()->Branch("QMisIDWeight_up",  &m_QMisIDWeight_UP_out, "QMisIDWeight_up/F");
      m_outputNTuple->tree()->Branch("QMisIDWeight_dn",  &m_QMisIDWeight_DN_out, "QMisIDWeight_dn/F");
  }

  if ( m_doMMWeighting ) {

      m_outputNTuple->tree()->Branch("MMWeight",	        &m_MMWeight_NOMINAL_out,	     "MMWeight/F");
      m_outputNTuple->tree()->Branch("MMWeight_lep0_r_stat_up", &m_weight_MM_lep0_R_stat_UP_out, "MMWeight_lep0_r_stat_up/F");
      m_outputNTuple->tree()->Branch("MMWeight_lep0_r_stat_dn", &m_weight_MM_lep0_R_stat_DN_out, "MMWeight_lep0_r_stat_dn/F");
      m_outputNTuple->tree()->Branch("MMWeight_lep1_r_stat_up", &m_weight_MM_lep1_R_stat_UP_out, "MMWeight_lep1_r_stat_up/F");
      m_outputNTuple->tree()->Branch("MMWeight_lep1_r_stat_dn", &m_weight_MM_lep1_R_stat_DN_out, "MMWeight_lep1_r_stat_dn/F");
      m_outputNTuple->tree()->Branch("MMWeight_lep0_f_stat_up", &m_weight_MM_lep0_F_stat_UP_out, "MMWeight_lep0_f_stat_up/F");
      m_outputNTuple->tree()->Branch("MMWeight_lep0_f_stat_dn", &m_weight_MM_lep0_F_stat_DN_out, "MMWeight_lep0_f_stat_dn/F");
      m_outputNTuple->tree()->Branch("MMWeight_lep1_f_stat_up", &m_weight_MM_lep1_F_stat_UP_out, "MMWeight_lep1_f_stat_up/F");
      m_outputNTuple->tree()->Branch("MMWeight_lep1_f_stat_dn", &m_weight_MM_lep1_F_stat_DN_out, "MMWeight_lep1_f_stat_dn/F");
      
      /*
      // Parse input weight list, split by comma, and put into a vector
      //
      std::vector<std::string> systematics;
      ANA_CHECK( this->tokenize( ',', systematics, m_systematics_list ) );

      // Initialise the map containing the variations of MM weights for each input systematics.
     
      for ( const auto& sys in systematics ) {
    	  m_MMWeight_out[sys] = std::vector<float>(8);
      }

      // Set output branch for the nominal weight
      
      m_outputNTuple->tree()->Branch("MMWeight", &m_MMWeight_NOMINAL_out, "MMWeight/F");
      
      // Set output branches for the variations of MM weight for each systematic.
      
      std::string key("");
      for ( auto& weight_map in m_MMWeight_out ) {
      
           key = weight_map.first();
	   
	   std::string branchname_0 = "MMWeight_lep0_r_" + key + "_up";
	   std::string branchname_1 = "MMWeight_lep0_r_" + key + "_dn";
	   std::string branchname_2 = "MMWeight_lep1_r_" + key + "_up";
	   std::string branchname_3 = "MMWeight_lep1_r_" + key + "_dn";     
	   std::string branchname_4 = "MMWeight_lep0_f_" + key + "_up";
	   std::string branchname_5 = "MMWeight_lep0_f_" + key + "_dn";
	   std::string branchname_6 = "MMWeight_lep1_f_" + key + "_up";
	   std::string branchname_7 = "MMWeight_lep1_f_" + key + "_dn"; 
 	
	   m_outputNTuple->tree()->Branch( (branchname_0).c_str(), &(weight_map.second.at(0)), (branchname_0.append("/F")).c_str() );
	   m_outputNTuple->tree()->Branch( (branchname_1).c_str(), &(weight_map.second.at(1)), (branchname_1.append("/F")).c_str() );
	   m_outputNTuple->tree()->Branch( (branchname_2).c_str(), &(weight_map.second.at(2)), (branchname_2.append("/F")).c_str() );
	   m_outputNTuple->tree()->Branch( (branchname_3).c_str(), &(weight_map.second.at(3)), (branchname_3.append("/F")).c_str() );
	   m_outputNTuple->tree()->Branch( (branchname_4).c_str(), &(weight_map.second.at(4)), (branchname_4.append("/F")).c_str() );
	   m_outputNTuple->tree()->Branch( (branchname_5).c_str(), &(weight_map.second.at(5)), (branchname_5.append("/F")).c_str() );
	   m_outputNTuple->tree()->Branch( (branchname_6).c_str(), &(weight_map.second.at(6)), (branchname_6.append("/F")).c_str() );
	   m_outputNTuple->tree()->Branch( (branchname_7).c_str(), &(weight_map.second.at(7)), (branchname_7.append("/F")).c_str() );

      }
      */
  }
  
  // ---------------------------------------------------------------------------------------------------------------

  // Initialise counter for input TTree entries
  //
  m_numEntry = 0;

  // Initialise counter for events where inf/nan is read
  //
  m_count_inf = 0;

  // ---------------------------------------------------------------------------------------------------------------

  m_outputNTuple->tree()->SetName( m_outputNTupName.c_str() );

  // ---------------------------------------------------------------------------------------------------------------

  // Copy input TTree weight to output TTree

  m_outputNTuple->tree()->SetWeight( m_inputNTuple->GetWeight() );

  // ---------------------------------------------------------------------------------------------------------------

  if ( m_doQMisIDWeighting ) {
      Info("initialize()","Reading QMisID rates from ROOT file(s)..");
      ANA_CHECK( this->readQMisIDRates() );
  }
  if ( m_doMMWeighting ) {
      Info("initialize()","Reading MM efficiencies from ROOT file(s)..");
      ANA_CHECK( this->readRFEfficiencies() );
  }

  // ---------------------------------------------------------------------------------------------------------------

  Info("initialize()", "All good!");

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode HTopMultilepNTupReprocesser :: execute ()
{
  // Here you do everything that needs to be done on every single
  // events, e.g. read input variables, apply cuts, and fill
  // histograms and trees.  This is where most of your actual analysis
  // code will go.

  ANA_CHECK_SET_TYPE (EL::StatusCode);

  if ( m_numEntry == 0 ) { Info("execute()", "Processing input TTree : %s\n", m_inputNTuple->GetName() ); }

  m_inputNTuple->GetEntry( wk()->treeEntry() );

  if ( m_debug ) { Info("execute()", "===> Entry %u - EventNumber = %u ", static_cast<uint32_t>(m_numEntry), static_cast<uint32_t>(m_EventNumber) ); }

  ++m_numEntry;

  if ( m_numEntry > 0 && ( static_cast<int>(m_numEntry) % 20000 == 0 ) ) { Info("execute()","Processed %u entries", static_cast<uint32_t>(m_numEntry)); }

  // ------------------------------------------------------------------------

  // This call is crucial, otherwise you'll get no entries in the output tree!
  //
  m_outputNTuple->setFilterPassed();

  // ------------------------------------------------------------------------

  m_event = std::make_shared<eventObj>();

  // ------------------------------------------------------------------------

  auto lep0 = std::make_shared<leptonObj>();

  lep0.get()->pt            = m_lep_Pt_0;
  lep0.get()->eta           = m_lep_Eta_0;
  lep0.get()->etaBE2        = m_lep_EtaBE2_0;
  lep0.get()->ID            = m_lep_ID_0;
  lep0.get()->flavour       = abs(m_lep_ID_0);
  lep0.get()->charge        = m_lep_ID_0 / fabs(m_lep_ID_0);
  lep0.get()->tightselected = m_lep_isTightSelected_0;
  lep0.get()->trigmatched   = m_lep_isTrigMatch_0;

  m_leptons.push_back(lep0);

  auto lep1 = std::make_shared<leptonObj>();

  lep1.get()->pt            = m_lep_Pt_1;
  lep1.get()->eta           = m_lep_Eta_1;
  lep1.get()->etaBE2        = m_lep_EtaBE2_1;
  lep1.get()->ID            = m_lep_ID_1;
  lep1.get()->flavour       = abs(m_lep_ID_1);
  lep1.get()->charge        = m_lep_ID_1 / fabs(m_lep_ID_1);
  lep1.get()->tightselected = m_lep_isTightSelected_1;
  lep1.get()->trigmatched   = m_lep_isTrigMatch_1;

  m_leptons.push_back(lep1);

  m_event.get()->isMC   = ( m_mc_channel_number > 0 );
  m_event.get()->dilep  = ( m_dilep_type > 0 );
  m_event.get()->isSS01 = ( m_isSS01 );

  m_event.get()->TT         = m_is_T_T;
  m_event.get()->TAntiT     = m_is_T_AntiT;
  m_event.get()->AntiTT     = m_is_AntiT_T;
  m_event.get()->AntiTAntiT = m_is_AntiT_AntiT;

  if ( m_debug ) {
      Info("execute()","lep0:\n pT = %.2f\n etaBE2 = %.2f\n eta = %.2f\n flavour = %i\n tight? %i\n trigmatched? %i", lep0.get()->pt/1e3, lep0.get()->etaBE2, lep0.get()->eta, lep0.get()->flavour, lep0.get()->tightselected, lep0.get()->trigmatched );
      Info("execute()","lep1:\n pT = %.2f\n etaBE2 = %.2f\n eta = %.2f\n flavour = %i\n tight? %i\n trigmatched? %i", lep1.get()->pt/1e3, lep1.get()->etaBE2, lep1.get()->eta, lep1.get()->flavour, lep1.get()->tightselected, lep1.get()->trigmatched );
      Info("execute()","event:\n TT ? %i, TAntiT ? %i, AntiTT ? %i, AntiTAntiT ? %i", m_event.get()->TT, m_event.get()->TAntiT, m_event.get()->AntiTT, m_event.get()->AntiTAntiT );
  }

  if ( m_debug ) {
      if ( m_doQMisIDWeighting ) {
	  if ( !m_isQMisIDBranchIn ) {
	      Info("execute()","\t\tDefault QMisIDWeight = %.3f", m_event.get()->weight_QMisID );
	      Info("execute()","\t\tDefault QMisIDWeight (up) = %.3f", m_event.get()->weight_QMisID_UP );
	      Info("execute()","\t\tDefault QMisIDWeight (dn) = %.3f", m_event.get()->weight_QMisID_DN );
	  } else {
	      Info("execute()","\t\tIN QMisIDWeight = %.3f", m_QMisIDWeight_in );
	      Info("execute()","\t\tIN QMisIDWeight (up) = %.3f", m_QMisIDWeight_UP_in );
	      Info("execute()","\t\tIN QMisIDWeight (dn) = %.3f", m_QMisIDWeight_DN_in );
	  }
      } 
      if ( m_doMMWeighting ) {
	  if ( !m_isMMBranchIn ) {
	      Info("execute()","\t\tDefault MMWeight = %.3f", m_event.get()->weight_MM );
	      Info("execute()","\t\tDefault MMWeight (lep0 r up) = %.3f", m_event.get()->weight_MM_lep0_R_stat_UP );
	      Info("execute()","\t\tDefault MMWeight (lep0 r dn) = %.3f", m_event.get()->weight_MM_lep0_R_stat_DN );
	      Info("execute()","\t\tDefault MMWeight (lep1 r up) = %.3f", m_event.get()->weight_MM_lep1_R_stat_UP );
	      Info("execute()","\t\tDefault MMWeight (lep1 r dn) = %.3f", m_event.get()->weight_MM_lep1_R_stat_DN );
	      Info("execute()","\t\tDefault MMWeight (lep0 f up) = %.3f", m_event.get()->weight_MM_lep0_F_stat_UP );
	      Info("execute()","\t\tDefault MMWeight (lep0 f dn) = %.3f", m_event.get()->weight_MM_lep0_F_stat_DN );
	      Info("execute()","\t\tDefault MMWeight (lep1 f up) = %.3f", m_event.get()->weight_MM_lep1_F_stat_UP );
	      Info("execute()","\t\tDefault MMWeight (lep1 f dn) = %.3f", m_event.get()->weight_MM_lep1_F_stat_DN );
	  } else {
	      Info("execute()","\t\tIN MMWeight = %.3f", m_MMWeight_in );
	      Info("execute()","\t\tIN MMWeight (lep0 r up) = %.3f", m_weight_MM_lep0_R_stat_UP_in );
	      Info("execute()","\t\tIN MMWeight (lep0 r dn) = %.3f", m_weight_MM_lep0_R_stat_DN_in );
	      Info("execute()","\t\tIN MMWeight (lep1 r up) = %.3f", m_weight_MM_lep1_R_stat_UP_in );
	      Info("execute()","\t\tIN MMWeight (lep1 r dn) = %.3f", m_weight_MM_lep1_R_stat_DN_in );
	      Info("execute()","\t\tIN MMWeight (lep0 f up) = %.3f", m_weight_MM_lep0_F_stat_UP_in );
	      Info("execute()","\t\tIN MMWeight (lep0 f dn) = %.3f", m_weight_MM_lep0_F_stat_DN_in );
	      Info("execute()","\t\tIN MMWeight (lep1 f up) = %.3f", m_weight_MM_lep1_F_stat_UP_in );
	      Info("execute()","\t\tIN MMWeight (lep1 f dn) = %.3f", m_weight_MM_lep1_F_stat_DN_in );
	  }
      }
  }

  // ------------------------------------------------------------------------

  if ( m_doQMisIDWeighting ) {
      ANA_CHECK( this->calculateQMisIDWeights () );
  }
  if ( m_doMMWeighting ) {
      ANA_CHECK( this->calculateMMWeights () );
  }

  // ------------------------------------------------------------------------

  ANA_CHECK( this->setOutputBranches() );

  // ------------------------------------------------------------------------

  if ( m_debug ) {
      if ( m_doQMisIDWeighting ) {
	  Info("execute()","\t\tOUT QMisIDWeight = %.3f", m_QMisIDWeight_out );
	  Info("execute()","\t\tOUT QMisIDWeight (up) = %.3f", m_QMisIDWeight_UP_out );
	  Info("execute()","\t\tOUT QMisIDWeight (dn) = %.3f", m_QMisIDWeight_DN_out );
      }
      if ( m_doMMWeighting ) {
	  Info("execute()","\t\tOUT MMWeight = %.3f", m_MMWeight_NOMINAL_out );
	  Info("execute()","\t\tOUT MMWeight (lep0 r up) * nominal = %.3f ( not rescaled = %.3f )", m_MMWeight_NOMINAL_out * m_weight_MM_lep0_R_stat_UP_out, m_weight_MM_lep0_R_stat_UP_out);
	  Info("execute()","\t\tOUT MMWeight (lep0 r dn) * nominal = %.3f ( not rescaled = %.3f )", m_MMWeight_NOMINAL_out * m_weight_MM_lep0_R_stat_DN_out, m_weight_MM_lep0_R_stat_DN_out);
	  Info("execute()","\t\tOUT MMWeight (lep1 r up) * nominal = %.3f ( not rescaled = %.3f )", m_MMWeight_NOMINAL_out * m_weight_MM_lep1_R_stat_UP_out, m_weight_MM_lep1_R_stat_UP_out);
	  Info("execute()","\t\tOUT MMWeight (lep1 r dn) * nominal = %.3f ( not rescaled = %.3f )", m_MMWeight_NOMINAL_out * m_weight_MM_lep1_R_stat_DN_out, m_weight_MM_lep1_R_stat_DN_out);
	  Info("execute()","\t\tOUT MMWeight (lep0 f up) * nominal = %.3f ( not rescaled = %.3f )", m_MMWeight_NOMINAL_out * m_weight_MM_lep0_F_stat_UP_out, m_weight_MM_lep0_F_stat_UP_out);
	  Info("execute()","\t\tOUT MMWeight (lep0 f dn) * nominal = %.3f ( not rescaled = %.3f )", m_MMWeight_NOMINAL_out * m_weight_MM_lep0_F_stat_DN_out, m_weight_MM_lep0_F_stat_DN_out);
	  Info("execute()","\t\tOUT MMWeight (lep1 f up) * nominal = %.3f ( not rescaled = %.3f )", m_MMWeight_NOMINAL_out * m_weight_MM_lep1_F_stat_UP_out, m_weight_MM_lep1_F_stat_UP_out);
	  Info("execute()","\t\tOUT MMWeight (lep1 f dn) * nominal = %.3f ( not rescaled = %.3f )", m_MMWeight_NOMINAL_out * m_weight_MM_lep1_F_stat_DN_out, m_weight_MM_lep1_F_stat_DN_out);  
      }
  }

  // ------------------------------------------------------------------------

  m_leptons.clear();

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode HTopMultilepNTupReprocesser :: postExecute ()
{
  // Here you do everything that needs to be done after the main event
  // processing.  This is typically very rare, particularly in user
  // code.  It is mainly used in implementing the NTupleSvc.

  //ANA_CHECK_SET_TYPE (EL::StatusCode);

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode HTopMultilepNTupReprocesser :: finalize ()
{
  // This method is the mirror image of initialize(), meaning it gets
  // called after the last event has been processed on the worker node
  // and allows you to finish up any objects you created in
  // initialize() before they are written to disk.  This is actually
  // fairly rare, since this happens separately for each worker node.
  // Most of the time you want to do your post-processing on the
  // submission node after all your histogram outputs have been
  // merged.  This is different from histFinalize() in that it only
  // gets called on worker nodes that processed input events.

  //ANA_CHECK_SET_TYPE (EL::StatusCode);

  Info("finalize()", "Finalising HTopMultilepNTupReprocesser...");

  Info("finalize()", "Events where inf/nan input was read: %u", m_count_inf );

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode HTopMultilepNTupReprocesser :: histFinalize ()
{
  // This method is the mirror image of histInitialize(), meaning it
  // gets called after the last event has been processed on the worker
  // node and allows you to finish up any objects you created in
  // histInitialize() before they are written to disk.  This is
  // actually fairly rare, since this happens separately for each
  // worker node.  Most of the time you want to do your
  // post-processing on the submission node after all your histogram
  // outputs have been merged.  This is different from finalize() in
  // that it gets called on all worker nodes regardless of whether
  // they processed input events.

  //ANA_CHECK_SET_TYPE (EL::StatusCode);

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode HTopMultilepNTupReprocesser :: enableSelectedBranches ()
{

  if ( m_inputBranches.empty() ) {
    Info("enableSelectedBranches()", "Keeping all branches enabled...");
    return EL::StatusCode::SUCCESS;
  }

  // Firstly, disable all branches
  //
  m_inputNTuple->SetBranchStatus ("*", 0);

  std::vector<std::string> branch_vec;

  // Parse input list, split by comma, and put into a vector
  //
  std::string token;
  std::istringstream ss( m_inputBranches );
  while ( std::getline(ss, token, ',') ) { branch_vec.push_back(token); }

  // Re-enable only the branches we are going to use
  //
  Info("enableSelectedBranches()", "Activating branches:\n");
  for ( const auto& branch : branch_vec ) {

    if ( !m_isQMisIDBranchIn && branch.find("QMisIDWeight") != std::string::npos ) { continue; }
    if ( !m_isMMBranchIn && branch.find("MMWeight") != std::string::npos )         { continue; }

    std::cout << "SetBranchStatus(" << branch << ", 1)" << std::endl;

    m_inputNTuple->SetBranchStatus (branch.c_str(), 1);

  }

  return EL::StatusCode::SUCCESS;

}


EL::StatusCode HTopMultilepNTupReprocesser :: setOutputBranches ()
{

  // Clear vector branches from previous event
  //
  ANA_CHECK( this->clearBranches() );

  if ( m_doQMisIDWeighting ) {
      m_QMisIDWeight_out    = m_event.get()->weight_QMisID;
      m_QMisIDWeight_UP_out = m_event.get()->weight_QMisID_UP;
      m_QMisIDWeight_DN_out = m_event.get()->weight_QMisID_DN;
  }
  if ( m_doMMWeighting ) {
      m_MMWeight_NOMINAL_out         = m_event.get()->weight_MM;
      m_weight_MM_lep0_R_stat_UP_out = m_event.get()->weight_MM_lep0_R_stat_UP;
      m_weight_MM_lep0_R_stat_DN_out = m_event.get()->weight_MM_lep0_R_stat_DN;
      m_weight_MM_lep1_R_stat_UP_out = m_event.get()->weight_MM_lep1_R_stat_UP;
      m_weight_MM_lep1_R_stat_DN_out = m_event.get()->weight_MM_lep1_R_stat_DN;
      m_weight_MM_lep0_F_stat_UP_out = m_event.get()->weight_MM_lep0_F_stat_UP;
      m_weight_MM_lep0_F_stat_DN_out = m_event.get()->weight_MM_lep0_F_stat_DN;
      m_weight_MM_lep1_F_stat_UP_out = m_event.get()->weight_MM_lep1_F_stat_UP;
      m_weight_MM_lep1_F_stat_DN_out = m_event.get()->weight_MM_lep1_F_stat_DN;
  }

  return EL::StatusCode::SUCCESS;

}

EL::StatusCode HTopMultilepNTupReprocesser :: clearBranches ()
{

  return EL::StatusCode::SUCCESS;

}

EL::StatusCode HTopMultilepNTupReprocesser ::  readQMisIDRates()
{
    if ( m_QMisIDRates_dir.back() != '/' ) { m_QMisIDRates_dir += "/"; }

    std::string path_AntiT = m_QMisIDRates_dir + m_QMisIDRates_Filename_AntiT;
    std::string path_T     = m_QMisIDRates_dir + m_QMisIDRates_Filename_T;

    TFile *file_AntiT = TFile::Open(path_AntiT.c_str());
    TFile *file_T     = TFile::Open(path_T.c_str());

    HTOP_RETURN_CHECK( "HTopMultilepNTupReprocesser::readQMisIDRates()", file_AntiT->IsOpen(), "Failed to open ROOT file" );
    HTOP_RETURN_CHECK( "HTopMultilepNTupReprocesser::readQMisIDRates()", file_T->IsOpen(), "Failed to open ROOT file" );

    Info("readQMisIDRates()", "Successfully opened ROOT files with QMisID rates from path:\n AntiT --> %s \n T --> %s", path_AntiT.c_str(), path_T.c_str() );

    TH2D *hist_QMisID_AntiT = get_object<TH2D>( *file_AntiT, "Rates" );
    TH2D *hist_QMisID_T     = get_object<TH2D>( *file_T, "Rates" );

    hist_QMisID_AntiT->SetDirectory(0);
    hist_QMisID_T->SetDirectory(0);

    // fill a map for later usage
    //
    m_QMisID_hist_map["AntiT"] = hist_QMisID_AntiT;
    m_QMisID_hist_map["T"]     = hist_QMisID_T;

    return EL::StatusCode::SUCCESS;
}

EL::StatusCode HTopMultilepNTupReprocesser :: calculateQMisIDWeights ()
{
    ANA_CHECK_SET_TYPE (EL::StatusCode);

    // If is not a dileptonic event, return
    //
    if ( m_dilep_type <= 0 ) { return EL::StatusCode::SUCCESS; }

    // If there are no electrons, return
    //
    if ( m_dilep_type == 1 ) { return EL::StatusCode::SUCCESS; }

    std::shared_ptr<leptonObj> el0;
    std::shared_ptr<leptonObj> el1;

    if ( m_dilep_type == 2 ) { // OF events
	el0 = ( m_leptons.at(0).get()->flavour == 11 ) ? m_leptons.at(0) : m_leptons.at(1);
    } else if ( m_dilep_type == 3 ) { // ee events
	el0 = m_leptons.at(0);
	el1 = m_leptons.at(1);
    }

    // Just a precaution...
    //
    if ( el0 && !( fabs(el0.get()->eta) < 2.5 && el0.get()->pt >= 0.0 ) ) { return EL::StatusCode::SUCCESS; }
    if ( el1 && !( fabs(el1.get()->eta) < 2.5 && el1.get()->pt >= 0.0 ) ) { return EL::StatusCode::SUCCESS; }

    float r0(0.0), r0_up(0.0), r0_dn(0.0), r1(0.0), r1_up(0.0), r1_dn(0.0);

    if ( m_useTAntiTRates ) {

	if ( el0 && el1 ) { // ee events
	    if ( el0.get()->tightselected && el1.get()->tightselected ) {
		ANA_CHECK( this->getQMisIDRatesAndError( el0, r0, r0_up, r0_dn, "TIGHT" ) );
		ANA_CHECK( this->getQMisIDRatesAndError( el1, r1, r1_up, r1_dn, "TIGHT" ) );
	    } else {
		ANA_CHECK( this->getQMisIDRatesAndError( el0, r0, r0_up, r0_dn, "ANTI_TIGHT" ) );
		ANA_CHECK( this->getQMisIDRatesAndError( el1, r1, r1_up, r1_dn, "ANTI_TIGHT" ) );
	    }
	} else { // OF events
	    if ( el0.get()->tightselected ) {
		ANA_CHECK( this->getQMisIDRatesAndError( el0, r0, r0_up, r0_dn, "TIGHT" ) );
	    } else {
		ANA_CHECK( this->getQMisIDRatesAndError( el0, r0, r0_up, r0_dn, "ANTI_TIGHT" ) );
	    }
	}

    } else {

	// Look at el0 first...
	//
	if ( el0.get()->tightselected ) {
	    ANA_CHECK( this->getQMisIDRatesAndError( el0, r0, r0_up, r0_dn, "TIGHT" ) );
	} else {
	    ANA_CHECK( this->getQMisIDRatesAndError( el0, r0, r0_up, r0_dn, "ANTI_TIGHT" ) );
	}
	// .. and now at el1 (if any...otherwise r1 weights will be default)
	//
	if ( el1 ) {
	    if (  el1.get()->tightselected ) {
		ANA_CHECK( this->getQMisIDRatesAndError( el1, r1, r1_up, r1_dn, "TIGHT" ) );
	    } else {
		ANA_CHECK( this->getQMisIDRatesAndError( el1, r1, r1_up, r1_dn, "ANTI_TIGHT" ) );
	    }
	}
    }

    if ( m_debug ) {
	Info("calculateQMisIDWeights()","\t r0 = %f ( up = %f, dn = %f )", r0, r0_up, r0_dn );
	Info("calculateQMisIDWeights()","\t r1 = %f ( up = %f, dn = %f )", r1, r1_up, r1_dn );
    }

    // Finally, store the event weight + (relative) variations
    //
    if ( !( std::isnan(r0) ) && !( std::isnan(r1) ) && !( std::isinf(r0) ) && !( std::isinf(r1) ) ) {

        float nominal = ( r0 + r1 - 2.0 * r0 * r1 ) / ( 1.0 - r0 - r1 + 2.0 * r0 * r1 );
        float up      = ( r0_up + r1_up - 2.0 * r0_up * r1_up ) / ( 1.0 - r0_up - r1_up + 2.0 * r0_up * r1_up );
        float dn      = ( r0_dn + r1_dn - 2.0 * r0_dn * r1_dn ) / ( 1.0 - r0_dn - r1_dn + 2.0 * r0_dn * r1_dn );

	m_event.get()->weight_QMisID    = nominal;
	m_event.get()->weight_QMisID_UP = ( !std::isnan(up/nominal) && !std::isinf(up/nominal) ) ? up/nominal : 0.0;
	m_event.get()->weight_QMisID_DN = ( !std::isnan(dn/nominal) && !std::isinf(dn/nominal) ) ? dn/nominal : 0.0;

    } else {
      ++m_count_inf;
    }

    return EL::StatusCode::SUCCESS;
}


EL::StatusCode HTopMultilepNTupReprocesser :: getQMisIDRatesAndError( std::shared_ptr<leptonObj> lep,
		                                     	              float& r, float& r_up, float& r_dn,
								      const std::string& selection )
{

    // Get the 2D histogram from the map
    //
    TH2D* rates_2D(nullptr);
    std::string name_eta(""), name_pt("");

    if ( selection.compare("TIGHT") == 0 ) {
      rates_2D = ( m_QMisID_hist_map.find("T")->second );
      name_eta = "proj_eta_T";
      name_pt  = "proj_pt_T";
    } else if ( selection.compare("ANTI_TIGHT") == 0 ) {
      rates_2D = ( m_QMisID_hist_map.find("AntiT")->second );
      name_eta = "proj_eta_AntiT";
      name_pt  = "proj_pt_AntiT";
    }

    // Make (eta,pT) projections of the 2D histogram with the rates
    //
    TH1D* proj_eta = rates_2D->ProjectionX(name_eta.c_str());
    TH1D* proj_pt  = rates_2D->ProjectionY(name_pt.c_str());

    float this_low_edge(-999.0),this_up_edge(-999.0);

    int eta_bin_nr(-1), pt_bin_nr(-1);

    float eta = lep.get()->etaBE2;
    float pt  = lep.get()->pt;

    // Loop over the projections, and keep track of the bin number where (x,y) is found
    //
    for ( int eta_bin = 0; eta_bin < proj_eta->GetNbinsX()+1; ++eta_bin  ) {

	this_low_edge = proj_eta->GetXaxis()->GetBinLowEdge(eta_bin);
	this_up_edge  = proj_eta->GetXaxis()->GetBinLowEdge(eta_bin+1);

	if ( fabs(eta) >= this_low_edge && fabs(eta) < this_up_edge ) {

	    if ( m_debug ) { Info("getQMisIDRatesAndError()","\t\t eta = %.2f found in %i-th bin", eta, eta_bin ); }

	    eta_bin_nr = proj_eta->GetBin(eta_bin);

	    break;
	}

    }
    for ( int pt_bin = 0; pt_bin < proj_pt->GetNbinsX()+1; ++ pt_bin ) {

	this_low_edge = proj_pt->GetXaxis()->GetBinLowEdge(pt_bin);
	this_up_edge  = proj_pt->GetXaxis()->GetBinLowEdge(pt_bin+1);

	if ( pt/1e3 >= this_low_edge && pt/1e3 < this_up_edge ) {

	    if ( m_debug ) { Info("getQMisIDRatesAndError()","\t\t pT = %.2f found in %i-th bin", pt/1e3, pt_bin ); }

	    pt_bin_nr = proj_pt->GetBin(pt_bin);

	    break;
	}

    }

    if ( m_debug ) { Info("getQMisIDRatesAndError()","\t\t coordinates of efficiency bin = (%i,%i)", eta_bin_nr, pt_bin_nr ); }

    // Now get the NOMINAL rate via global bin number (x,y)

    r = rates_2D->GetBinContent( rates_2D->GetBin( eta_bin_nr, pt_bin_nr ) );

    if ( std::isnan(r) ) {
	Warning("getQMisIDRatesAndError()", "Rate value being read in is nan. Will assign default QMisIDWeight...");
	return EL::StatusCode::SUCCESS;
    }
    if ( std::isinf(r) ) {
	Warning("getQMisIDRatesAndError()", "Rate value being read in is inf. Will assign default QMisIDWeight...");
	return EL::StatusCode::SUCCESS;
    }

    // Get the UP and DOWN variations
    //
    // QUESTION: Why the hell ROOT has GetBinErrorUp and GetBinErrorLow for TH2 ??
    // They seem to give always the same result...
    //
    r_up = r + rates_2D->GetBinErrorUp( rates_2D->GetBin( eta_bin_nr, pt_bin_nr ) );
    r_dn = r - rates_2D->GetBinErrorUp( rates_2D->GetBin( eta_bin_nr, pt_bin_nr ) );
    r_dn = ( r_dn > 0.0 ) ? r_dn : 0.0;

    return EL::StatusCode::SUCCESS;

}

EL::StatusCode HTopMultilepNTupReprocesser :: readRFEfficiencies()
{

  std::string rate_type = ( !m_doMMClosure ) ? "observed" : "expected";

  if ( m_FEFF_dir.empty() ) { m_FEFF_dir = m_REFF_dir; }

  if ( m_REFF_dir.back() != '/' ) { m_REFF_dir += "/"; }
  if ( m_FEFF_dir.back() != '/' ) { m_FEFF_dir += "/"; }

  // Histogram names - electrons
  //
  std::string histname_el_pt_reff  = "El_ProbePt_Real_Efficiency_"  + rate_type;
  std::string histname_el_eta_reff = "El_ProbeEta_Real_Efficiency_" + rate_type;
  std::string teffname_el_pt_reff  = "El_ProbePt_Real_TEfficiency_"  + rate_type;
  std::string teffname_el_eta_reff = "El_ProbeEta_Real_TEfficiency_" + rate_type;

  std::string histname_el_pt_r_T   = "El_ProbePt_Real_T_" + rate_type;
  std::string histname_el_pt_r_L   = "El_ProbePt_Real_L_" + rate_type;

  std::string histname_el_pt_feff(""), histname_el_eta_feff(""), histname_el_pt_f_T(""), histname_el_pt_f_L("");

  if ( m_useScaledFakeEfficiency && !m_doMMClosure ) {
    histname_el_pt_feff	 = "El_ProbePt_ScaledFake_Efficiency_"  + rate_type;
    histname_el_eta_feff = "El_ProbeEta_ScaledFake_Efficiency_" + rate_type;
    histname_el_pt_f_T   = "El_ProbePt_ScaledFake_T_" + rate_type;
    histname_el_pt_f_L   = "El_ProbePt_ScaledFake_L_" + rate_type;
  } else {
    histname_el_pt_feff  = "El_ProbePt_Fake_Efficiency_"  + rate_type;
    histname_el_eta_feff = "El_ProbeEta_Fake_Efficiency_" + rate_type;
    histname_el_pt_f_T   = "El_ProbePt_Fake_T_" + rate_type;
    histname_el_pt_f_L   = "El_ProbePt_Fake_L_" + rate_type;
  }
  std::string teffname_el_pt_feff  = "El_ProbePt_Fake_TEfficiency_"  + rate_type;
  std::string teffname_el_eta_feff = "El_ProbeEta_Fake_TEfficiency_" + rate_type;

  // Histogram names - muons
  //
  std::string histname_mu_pt_reff  = "Mu_ProbePt_Real_Efficiency_"  + rate_type;
  std::string histname_mu_eta_reff = "Mu_ProbeEta_Real_Efficiency_" + rate_type;
  std::string teffname_mu_pt_reff  = "Mu_ProbePt_Real_TEfficiency_"  + rate_type;
  std::string teffname_mu_eta_reff = "Mu_ProbeEta_Real_TEfficiency_" + rate_type;
  std::string histname_mu_pt_r_T   = "Mu_ProbePt_Real_T_" + rate_type;
  std::string histname_mu_pt_r_L   = "Mu_ProbePt_Real_L_" + rate_type;

  std::string histname_mu_pt_feff  = "Mu_ProbePt_Fake_Efficiency_"  + rate_type;
  std::string histname_mu_eta_feff = "Mu_ProbeEta_Fake_Efficiency_" + rate_type;
  std::string teffname_mu_pt_feff  = "Mu_ProbePt_Fake_TEfficiency_"  + rate_type;
  std::string teffname_mu_eta_feff = "Mu_ProbeEta_Fake_TEfficiency_" + rate_type;
  std::string histname_mu_pt_f_T   = "Mu_ProbePt_Fake_T_" + rate_type;
  std::string histname_mu_pt_f_L   = "Mu_ProbePt_Fake_L_" + rate_type;

  // Histograms - electrons

  TH1D *hist_el_pt_reff(nullptr);
  TH1D *hist_el_eta_reff(nullptr);
  TH1D *hist_el_pt_r_T(nullptr);
  TH1D *hist_el_pt_r_L(nullptr);

  TH1D *hist_el_pt_reff_YES_TM(nullptr);
  TH1D *hist_el_pt_reff_NO_TM(nullptr);

  TH1D *hist_el_pt_feff(nullptr);
  TH1D *hist_el_eta_feff(nullptr);
  TH1D *hist_el_pt_f_T(nullptr);
  TH1D *hist_el_pt_f_L(nullptr);

  TH1D *hist_el_pt_feff_YES_TM(nullptr);
  TH1D *hist_el_pt_feff_NO_TM(nullptr);

  TEfficiency *teff_el_pt_reff(nullptr);
  TEfficiency *teff_el_eta_reff(nullptr);

  TEfficiency *teff_el_pt_feff(nullptr);
  TEfficiency *teff_el_eta_feff(nullptr);

  // Histograms - muons

  TH1D *hist_mu_pt_reff(nullptr);
  TH1D *hist_mu_eta_reff(nullptr);
  TH1D *hist_mu_pt_r_T(nullptr);
  TH1D *hist_mu_pt_r_L(nullptr);

  TH1D *hist_mu_pt_reff_YES_TM(nullptr);
  TH1D *hist_mu_pt_reff_NO_TM(nullptr);

  TH1D *hist_mu_pt_feff(nullptr);
  TH1D *hist_mu_eta_feff(nullptr);
  TH1D *hist_mu_pt_f_T(nullptr);
  TH1D *hist_mu_pt_f_L(nullptr);

  TH1D *hist_mu_pt_feff_YES_TM(nullptr);
  TH1D *hist_mu_pt_feff_NO_TM(nullptr);

  TEfficiency *teff_mu_pt_reff(nullptr);
  TEfficiency *teff_mu_eta_reff(nullptr);

  TEfficiency *teff_mu_pt_feff(nullptr);
  TEfficiency *teff_mu_eta_feff(nullptr);

  // 1. 'REAL' efficiency

  Info("readRFEfficiencies()", "REAL efficiency from directory: %s ", m_REFF_dir.c_str() );

  std::string path_R_el = m_REFF_dir + m_Efficiency_Filename;
  TFile *file_R_el = TFile::Open(path_R_el.c_str());

  HTOP_RETURN_CHECK( "HTopMultilepNTupReprocesser::readRFEfficiencies()", file_R_el->IsOpen(), "Failed to open ROOT file" );
  Info("readRFEfficiencies()", "ELECTRON REAL efficiency: %s ", path_R_el.c_str() );

  std::string path_R_mu = m_REFF_dir + m_Efficiency_Filename;
  TFile *file_R_mu = TFile::Open(path_R_mu.c_str());

  HTOP_RETURN_CHECK( "HTopMultilepNTupReprocesser::readRFEfficiencies()", file_R_mu->IsOpen(), "Failed to open ROOT file" );
  Info("readRFEfficiencies()", "MUON REAL efficiency: %s ", path_R_mu.c_str() );

  // Get real efficiency histograms
  //
  hist_el_pt_reff  = get_object<TH1D>( *file_R_el, histname_el_pt_reff );
  teff_el_pt_reff  = get_object<TEfficiency>( *file_R_el, teffname_el_pt_reff );
  if( m_useEtaParametrisation ) {
      hist_el_eta_reff = get_object<TH1D>( *file_R_el, histname_el_eta_reff );
      teff_el_eta_reff = get_object<TEfficiency>( *file_R_el, teffname_el_eta_reff );
  }
  hist_el_pt_r_T = get_object<TH1D>( *file_R_el, histname_el_pt_r_T );
  hist_el_pt_r_L = get_object<TH1D>( *file_R_el, histname_el_pt_r_L );

  hist_mu_pt_reff  = get_object<TH1D>( *file_R_mu, histname_mu_pt_reff );
  teff_mu_pt_reff  = get_object<TEfficiency>( *file_R_mu, teffname_mu_pt_reff );
  if ( m_useEtaParametrisation ) {
      hist_mu_eta_reff = get_object<TH1D>( *file_R_mu, histname_mu_eta_reff );
      teff_mu_eta_reff = get_object<TEfficiency>( *file_R_mu, teffname_mu_eta_reff );
  }
  hist_mu_pt_r_T = get_object<TH1D>( *file_R_mu, histname_mu_pt_r_T );
  hist_mu_pt_r_L = get_object<TH1D>( *file_R_mu, histname_mu_pt_r_L );

  // 2. FAKE efficiency

  if ( m_FEFF_dir.compare(m_REFF_dir) != 0 ) {
     Warning("readRFEfficiencies()", "FAKE efficiency is going to be read from %s. Check whether it's really what you want...", m_FEFF_dir.c_str());
  } else {
     Info("readRFEfficiencies()", "FAKE efficiency from same directory as REAL" );
  }

  std::string path_F_el = m_FEFF_dir + m_Efficiency_Filename;
  TFile *file_F_el = TFile::Open(path_F_el.c_str());

  HTOP_RETURN_CHECK( "HTopMultilepNTupReprocesser::readRFEfficiencies()", file_F_el->IsOpen(), "Failed to open ROOT file" );
  Info("readRFEfficiencies()", "ELECTRON FAKE efficiency: %s ", path_F_el.c_str() );

  std::string path_F_mu = m_FEFF_dir + m_Efficiency_Filename;
  TFile *file_F_mu = TFile::Open(path_F_mu.c_str());

  HTOP_RETURN_CHECK( "HTopMultilepNTupReprocesser::readRFEfficiencies()", file_F_mu->IsOpen(), "Failed to open ROOT file" );
  Info("readRFEfficiencies()", "MUON FAKE efficiency: %s ", path_F_mu.c_str() );

  // Get fake efficiency histograms
  //
  hist_el_pt_feff  = get_object<TH1D>( *file_F_el, histname_el_pt_feff );
  teff_el_pt_feff  = get_object<TEfficiency>( *file_R_el, teffname_el_pt_feff );
  if ( m_useEtaParametrisation ) {
      hist_el_eta_feff = get_object<TH1D>( *file_F_el, histname_el_eta_feff );
      teff_el_eta_feff = get_object<TEfficiency>( *file_R_el, teffname_el_eta_feff );
  }
  hist_el_pt_f_T   = get_object<TH1D>( *file_F_el, histname_el_pt_f_T );
  hist_el_pt_f_L   = get_object<TH1D>( *file_F_el, histname_el_pt_f_L );

  hist_mu_pt_feff    = get_object<TH1D>( *file_F_mu, histname_mu_pt_feff );
  teff_mu_pt_feff  = get_object<TEfficiency>( *file_R_mu, teffname_mu_pt_feff );
  if ( m_useEtaParametrisation ) {
      hist_mu_eta_feff = get_object<TH1D>( *file_F_mu, histname_mu_eta_feff );
      teff_mu_eta_feff = get_object<TEfficiency>( *file_R_mu, teffname_mu_eta_feff );
  }
  hist_mu_pt_f_T   = get_object<TH1D>( *file_F_mu, histname_mu_pt_f_T );
  hist_mu_pt_f_L   = get_object<TH1D>( *file_F_mu, histname_mu_pt_f_L );

  // ***********************************************************************

  if ( m_useTrigMatchingInfo && m_useEtaParametrisation ) {
      Error("readRFEfficiencies()", "As of today, it's not possible to use eta parametrisation when reading trigger-matching-dependent efficiencies. Aborting" );
      return EL::StatusCode::FAILURE;
  }

  if ( m_useTrigMatchingInfo ) {

    if ( m_EFF_YES_TM_dir.back() != '/' ) { m_EFF_YES_TM_dir += "/"; }
    if ( m_EFF_NO_TM_dir.back() != '/' )  { m_EFF_NO_TM_dir += "/"; }

    Info("readRFEfficiencies()", "REAL/FAKE efficiency (probe TRIGGER-MATCHED) from directory: %s ", m_EFF_YES_TM_dir.c_str() );

    std::string path_YES_TM = m_EFF_YES_TM_dir + m_Efficiency_Filename;
    TFile *file_YES_TM = TFile::Open(path_YES_TM.c_str());
    HTOP_RETURN_CHECK( "HTopMultilepNTupReprocesser::readRFEfficiencies()", file_YES_TM->IsOpen(), "Failed to open ROOT file" );
    Info("readRFEfficiencies()", "REAL/FAKE efficiency: %s ", path_YES_TM.c_str() );

    Info("readRFEfficiencies()", "REAL/FAKE efficiency (probe NOT TRIGGER-MATCHED) from directory: %s ", m_EFF_NO_TM_dir.c_str() );

    std::string path_NO_TM = m_EFF_NO_TM_dir + m_Efficiency_Filename;
    TFile *file_NO_TM = TFile::Open(path_NO_TM.c_str());
    HTOP_RETURN_CHECK( "HTopMultilepNTupReprocesser::readRFEfficiencies()", file_NO_TM->IsOpen(), "Failed to open ROOT file" );
    Info("readRFEfficiencies()", "REAL/FAKE efficiency: %s ", path_NO_TM.c_str() );

    // Get real efficiency histograms
    //
    hist_el_pt_reff_YES_TM = get_object<TH1D>( *file_YES_TM, histname_el_pt_reff );
    hist_el_pt_reff_NO_TM  = get_object<TH1D>( *file_NO_TM, histname_el_pt_reff );

    hist_mu_pt_reff_YES_TM = get_object<TH1D>( *file_YES_TM, histname_mu_pt_reff );
    hist_mu_pt_reff_NO_TM  = get_object<TH1D>( *file_NO_TM, histname_mu_pt_reff );

    // Get fake efficiency histograms
    //
    hist_el_pt_feff_YES_TM = get_object<TH1D>( *file_YES_TM, histname_el_pt_feff );
    hist_el_pt_feff_NO_TM  = get_object<TH1D>( *file_NO_TM, histname_el_pt_feff );

    hist_mu_pt_feff_YES_TM = get_object<TH1D>( *file_YES_TM, histname_mu_pt_feff );
    hist_mu_pt_feff_NO_TM  = get_object<TH1D>( *file_NO_TM, histname_mu_pt_feff );

  }
  // ***********************************************************************

  // Fill maps for later usage

  m_el_teff_map["pt_reff"]   = teff_el_pt_reff;
  m_mu_teff_map["pt_reff"]   = teff_mu_pt_reff;
  m_el_teff_map["pt_feff"]   = teff_el_pt_feff;
  m_mu_teff_map["pt_feff"]   = teff_mu_pt_feff;
  
  if ( m_useEtaParametrisation ) {
      m_el_teff_map["eta_reff"]  = teff_el_eta_reff;
      m_mu_teff_map["eta_reff"]  = teff_mu_eta_reff;
      m_el_teff_map["eta_feff"]  = teff_el_eta_feff;
      m_mu_teff_map["eta_feff"]  = teff_mu_eta_feff;
  }

  // Save in the histogram map a clone of the denominator histogram associated to the TEfficiency object in order to access the axis binning
  // If we are not using TEfficiency, take the TH1 efficiency histogram itself
  //
  // NB: Calling GetCopyTotalHisto() transfer the ownership of the histogram pointer to the user. This intoroduces a memory leak in the code,
  // as we don't explicitly call delete anywhere. However, this is harmless, since this is executed only once in the job.
  //
  m_el_hist_map["pt_reff_hist"] = ( m_useTEfficiency ) ? dynamic_cast<TH1D*>( teff_el_pt_reff->GetCopyTotalHisto() ) : hist_el_pt_reff;
  m_mu_hist_map["pt_reff_hist"] = ( m_useTEfficiency ) ? dynamic_cast<TH1D*>( teff_mu_pt_reff->GetCopyTotalHisto() ) : hist_mu_pt_reff;
  m_el_hist_map["pt_feff_hist"] = ( m_useTEfficiency ) ? dynamic_cast<TH1D*>( teff_el_pt_feff->GetCopyTotalHisto() ) : hist_el_pt_feff;
  m_mu_hist_map["pt_feff_hist"] = ( m_useTEfficiency ) ? dynamic_cast<TH1D*>( teff_mu_pt_feff->GetCopyTotalHisto() ) : hist_mu_pt_feff;
  
  if ( m_useEtaParametrisation ) {
      m_el_hist_map["eta_reff_hist"] = ( m_useTEfficiency ) ? dynamic_cast<TH1D*>( teff_el_eta_reff->GetCopyTotalHisto() ) : hist_el_eta_reff;
      m_mu_hist_map["eta_reff_hist"] = ( m_useTEfficiency ) ? dynamic_cast<TH1D*>( teff_mu_eta_reff->GetCopyTotalHisto() ) : hist_mu_eta_reff;
      m_el_hist_map["eta_feff_hist"] = ( m_useTEfficiency ) ? dynamic_cast<TH1D*>( teff_el_eta_feff->GetCopyTotalHisto() ) : hist_el_eta_feff;
      m_mu_hist_map["eta_feff_hist"] = ( m_useTEfficiency ) ? dynamic_cast<TH1D*>( teff_mu_eta_feff->GetCopyTotalHisto() ) : hist_mu_eta_feff;
  }

  m_el_hist_map["pt_reff_YES_TM"] = hist_el_pt_reff_YES_TM;
  m_mu_hist_map["pt_reff_YES_TM"] = hist_mu_pt_reff_YES_TM;
  m_el_hist_map["pt_feff_YES_TM"] = hist_el_pt_feff_YES_TM;
  m_mu_hist_map["pt_feff_YES_TM"] = hist_mu_pt_feff_YES_TM;
  m_el_hist_map["pt_reff_NO_TM"]  = hist_el_pt_reff_NO_TM;
  m_mu_hist_map["pt_reff_NO_TM"]  = hist_mu_pt_reff_NO_TM;
  m_el_hist_map["pt_feff_NO_TM"]  = hist_el_pt_feff_NO_TM;
  m_mu_hist_map["pt_feff_NO_TM"]  = hist_mu_pt_feff_NO_TM;

  // eta hist has same binning for r/f
  //
  if ( m_useEtaParametrisation ) {

      // Calculate normalisation factor for (pT * eta) 1D efficiencies case.
      //
      // This factor is the same for eta and pT r/f histograms (it's just Integral(N) / Integral(D) for the efficiency definition ): use pT
      //
      m_el_reff_tot = ( hist_el_pt_r_T->Integral(1,hist_el_pt_r_T->GetNbinsX()+1) ) / ( hist_el_pt_r_L->Integral(1,hist_el_pt_r_L->GetNbinsX()+1) );
      m_el_feff_tot = ( hist_el_pt_f_T->Integral(1,hist_el_pt_f_T->GetNbinsX()+1) ) / ( hist_el_pt_f_L->Integral(1,hist_el_pt_f_L->GetNbinsX()+1) );
      m_mu_reff_tot = ( hist_mu_pt_r_T->Integral(1,hist_mu_pt_r_T->GetNbinsX()+1) ) / ( hist_mu_pt_r_L->Integral(1,hist_mu_pt_r_L->GetNbinsX()+1) );
      m_mu_feff_tot = ( hist_mu_pt_f_T->Integral(1,hist_mu_pt_f_T->GetNbinsX()+1) ) / ( hist_mu_pt_f_L->Integral(1,hist_mu_pt_f_L->GetNbinsX()+1) );

  }

  std::cout << "\n" << std::endl;
  if ( m_useTEfficiency ) {
    Info("readRFEfficiencies()", "MUON REAL efficiency - pT TEfficiency name: %s ", teffname_mu_pt_reff.c_str() );
    Info("readRFEfficiencies()", "MUON FAKE efficiency - pT TEfficiency name: %s ", teffname_mu_pt_feff.c_str() );
    if ( m_useEtaParametrisation ) {
      Info("readRFEfficiencies()", "MUON REAL efficiency - eta TEfficiency name: %s ", teffname_mu_eta_reff.c_str() );
      Info("readRFEfficiencies()", "MUON FAKE efficiency - eta TEfficiency name: %s ", teffname_mu_eta_feff.c_str() );
    }
    std::cout << "	      --------------------------------------------" << std::endl;
    Info("readRFEfficiencies()", "ELECTRON REAL efficiency - pT TEfficiency name: %s ", teffname_el_pt_reff.c_str() );
    Info("readRFEfficiencies()", "ELECTRON FAKE efficiency - pT TEfficiency name: %s ", teffname_el_pt_feff.c_str() );
    if ( m_useEtaParametrisation ) {
      Info("readRFEfficiencies()", "ELECTRON REAL efficiency - eta TEfficiency name: %s ", teffname_el_eta_reff.c_str() );
      Info("readRFEfficiencies()", "ELECTRON FAKE efficiency - eta TEfficiency name: %s ", teffname_el_eta_feff.c_str() );
    }
  
  } else {
    Info("readRFEfficiencies()", "MUON REAL efficiency - pT TH1D name: %s ", histname_mu_pt_reff.c_str() );
    Info("readRFEfficiencies()", "MUON FAKE efficiency - pT TH1D name: %s ", histname_mu_pt_feff.c_str() );
    if ( m_useEtaParametrisation ) {
      Info("readRFEfficiencies()", "MUON REAL efficiency - eta TH1D name: %s ", histname_mu_eta_reff.c_str() );
      Info("readRFEfficiencies()", "MUON FAKE efficiency - eta TH1D name: %s ", histname_mu_eta_feff.c_str() );
    }
    std::cout << "	      --------------------------------------------" << std::endl;
    Info("readRFEfficiencies()", "ELECTRON REAL efficiency - pT TH1D name: %s ", histname_el_pt_reff.c_str() );
    Info("readRFEfficiencies()", "ELECTRON FAKE efficiency - pT TH1D name: %s ", histname_el_pt_feff.c_str() );
    if ( m_useEtaParametrisation ) {
      Info("readRFEfficiencies()", "ELECTRON REAL efficiency - eta TH1D name: %s ", histname_el_eta_reff.c_str() );
      Info("readRFEfficiencies()", "ELECTRON FAKE efficiency - eta TH1D name: %s ", histname_el_eta_feff.c_str() );
    }
  }
  std::cout << "\n" << std::endl;

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode HTopMultilepNTupReprocesser :: getMMEfficiencyAndError( std::shared_ptr<leptonObj> lep, std::vector<float>& efficiency, const std::string& type )
{

    float error_up(0.0), error_dn(0.0);

    float pt  = lep.get()->pt/1e3; // Must be in GeV!
    float eta = ( lep.get()->flavour == 13 ) ? lep.get()->eta : lep.get()->etaBE2;

    float this_low_edge_pt(-1.0), this_up_edge_pt(-1.0);
    float this_low_edge_eta(-999.0), this_up_edge_eta(-999.0);

    std::map< std::string, TH1D* >        *histograms    = ( lep.get()->flavour == 13 ) ? &m_mu_hist_map : &m_el_hist_map;
    std::map< std::string, TEfficiency* > *tefficiencies = ( lep.get()->flavour == 13 ) ? &m_mu_teff_map : &m_el_teff_map;

    TH1D *hist_pt(nullptr);  
    TH1D *hist_eta(nullptr); 
    
    TEfficiency *teff_pt(nullptr);  
    TEfficiency *teff_eta (nullptr);

    //  1) Fake case: choose appropriate histogram
    //
    if ( type.compare("FAKE") == 0 ) {

    	if ( m_verbose ) { Info("getMMEfficiencyAndError()", "\tReading fake efficiency..."); }
	    
	hist_pt = histograms->find("pt_feff_hist")->second;
	teff_pt = tefficiencies->find("pt_feff")->second;
	
	if ( m_useTrigMatchingInfo ) {
	    hist_pt = ( lep.get()->trigmatched ) ? histograms->find("pt_feff_YES_TM")->second : histograms->find("pt_feff_NO_TM")->second;
	}

	if ( m_useEtaParametrisation ) {
	    hist_eta = histograms->find("eta_feff_hist")->second;
            teff_eta = tefficiencies->find("eta_feff")->second;
	}

	// Loop over number of pt bins
    	// Do not consider underflow, i.e. 0th bin
    	//
    	for ( int p(1); p <= hist_pt->GetNbinsX()+1; ++p ) {

    	    this_low_edge_pt = hist_pt->GetXaxis()->GetBinLowEdge(p);
    	    this_up_edge_pt  = hist_pt->GetXaxis()->GetBinLowEdge(p+1);

    	    if ( m_verbose ) { Info("getMMEfficiencyAndError()","\t\tpT bin %i : [%.0f,%.0f] GeV", p, this_low_edge_pt, this_up_edge_pt ); }

    	    if ( pt >= this_low_edge_pt && pt < this_up_edge_pt ) {

    	        float feff_pt(1.0), feff_pt_err_up(0.0), feff_pt_err_dn(0.0);

		if ( m_useTEfficiency ) {
		     feff_pt	    = teff_pt->GetEfficiency(p);
		     feff_pt_err_up = teff_pt->GetEfficiencyErrorUp(p);
		     feff_pt_err_dn = teff_pt->GetEfficiencyErrorLow(p);
		} else {
		     feff_pt	    = hist_pt->GetBinContent(p);
		     feff_pt_err_up = feff_pt_err_dn = hist_pt->GetBinError(p);
                }

      	        if ( m_verbose ) { Info("getMMEfficiencyAndError()", "\t\tLepton pT = %.3f GeV ==> Reading fake efficiency in pT bin [%.0f,%.0f] GeV: feff_pt = %.3f", pt, this_low_edge_pt, this_up_edge_pt, feff_pt ); }

    	        float feff_eta(1.0), feff_eta_err_up(0.0), feff_eta_err_dn(0.0);

    	        if ( m_useEtaParametrisation ) {

	    	    // Loop over number of eta bins
    	            // Do not consider underflow, i.e. 0th bin
    	            //
    	            for ( int e(1); e <= hist_eta->GetNbinsX()+1; ++e ) {

	    	  	this_low_edge_eta = hist_eta->GetXaxis()->GetBinLowEdge(e);
    	        	this_up_edge_eta  = hist_eta->GetXaxis()->GetBinLowEdge(e+1);

    	        	if ( m_verbose ) { Info("getMMEfficiencyAndError()","\t\t|eta| bin %i : [%.3f,%.3f]", e, this_low_edge_eta, this_up_edge_eta ); }

    	        	if ( fabs(eta) >= this_low_edge_eta && fabs(eta) < this_up_edge_eta ) {

		 	    if ( m_useTEfficiency ) {
		 		 feff_eta	 = teff_eta->GetEfficiency(e);
		 		 feff_eta_err_up = teff_eta->GetEfficiencyErrorUp(e);
		 		 feff_eta_err_dn = teff_eta->GetEfficiencyErrorLow(e);
		 	    } else {
		 		 feff_eta        = hist_eta->GetBinContent(e);
		 		 feff_eta_err_up = feff_eta_err_dn = hist_eta->GetBinError(e);
                 	    }

			    if ( m_verbose ) {
    	        		Info("getMMEfficiencyAndError()", "\t\tLepton |eta| = %.3f ==> Reading fake efficiency in |eta| bin [%.3f,%.3f]: feff_eta = %.3f", fabs(eta), this_low_edge_eta, this_up_edge_eta, feff_eta );
    	        	    }

    	        	    break;
    	        	}
    	            }
    	        }

    	        // Nominal
    	        //
    	        efficiency.at(0) = feff_pt;
    	        error_up	 = feff_pt_err_up;
    	        error_dn	 = feff_pt_err_dn;

    	        // UP syst
    	        //
    	        efficiency.at(1) = ( feff_pt + error_up );

    	        // DN syst
    	        //
    	        if ( feff_pt - error_dn > 0 ) { efficiency.at(2) = ( feff_pt - error_dn ); }
    	        else			      { efficiency.at(2) = 0.0; }

    	        if ( m_useEtaParametrisation ) {

	    	    float feff_tot = ( lep.get()->flavour == 13 ) ? m_mu_feff_tot : m_el_feff_tot;
    	            if ( m_verbose ) {Info("getMMEfficiencyAndError()", "\t\t norm factor = %.3f", feff_tot ); }

	    	    efficiency.at(0) = ( feff_pt * feff_eta ) / feff_tot;

	    	    // Assuming  feff_pt,feff_eta are independent, this is the error on the product
    	            // ( the constant factor at denominator will be put back later in the def of Efficiency...)
    	            //
    	            error_up         = sqrt( (feff_eta*feff_pt_err_up)*(feff_eta*feff_pt_err_up) + (feff_pt*feff_eta_err_up)*(feff_pt*feff_eta_err_up) );
    	            error_dn         = sqrt( (feff_eta*feff_pt_err_dn)*(feff_eta*feff_pt_err_dn) + (feff_pt*feff_eta_err_dn)*(feff_pt*feff_eta_err_dn) );

    	            efficiency.at(1) = ( (feff_pt * feff_eta) + error_up ) / feff_tot;
    	            if ( (feff_pt * feff_eta) - error_dn > 0 ) { efficiency.at(2) = ( (feff_pt * feff_eta) - error_dn ) / feff_tot;}
    	            else				       { efficiency.at(2) = 0.0; }
    	        }

    	        break;
    	    }

    	} // close loop on pT bins: fake case

    }
    //  2) Real case: choose appropriate histogram
    //
    else if ( type.compare("REAL") == 0 ) {

    	if ( m_verbose ) { Info("getMMEfficiencyAndError()", "\tReading real efficiency..."); }

	hist_pt = histograms->find("pt_reff_hist")->second;
	teff_pt = tefficiencies->find("pt_reff")->second;
	
	if ( m_useTrigMatchingInfo ) {
	    hist_pt = ( lep.get()->trigmatched ) ? histograms->find("pt_reff_YES_TM")->second : histograms->find("pt_reff_NO_TM")->second;
	}

	if ( m_useEtaParametrisation ) {
	    hist_eta = histograms->find("eta_reff_hist")->second;
	    teff_eta = tefficiencies->find("eta_reff")->second;
	}

	// Loop over number of pt bins
    	// Do not consider underflow, i.e. 0th bin
    	//
    	for ( int p(1); p <= hist_pt->GetNbinsX()+1; ++p ) {

    	    this_low_edge_pt = hist_pt->GetXaxis()->GetBinLowEdge(p);
    	    this_up_edge_pt  = hist_pt->GetXaxis()->GetBinLowEdge(p+1);

    	    if ( m_verbose ) { Info("getMMEfficiencyAndError()","\t\tpT bin %i : [%.0f,%.0f] GeV", p, this_low_edge_pt, this_up_edge_pt ); }

    	    if ( pt >= this_low_edge_pt && pt < this_up_edge_pt ) {

    	        float reff_pt(1.0), reff_pt_err_up(0.0), reff_pt_err_dn(0.0);

		if ( m_useTEfficiency ) {
		     reff_pt	    = teff_pt->GetEfficiency(p);
		     reff_pt_err_up = teff_pt->GetEfficiencyErrorUp(p);
		     reff_pt_err_dn = teff_pt->GetEfficiencyErrorLow(p);
		} else {
		     reff_pt	    = hist_pt->GetBinContent(p);
		     reff_pt_err_up = reff_pt_err_dn = hist_pt->GetBinError(p);
                }

      	        if ( m_verbose ) { Info("getMMEfficiencyAndError()", "\t\tLepton pT = %.3f GeV ==> Reading real efficiency in pT bin [%.0f,%.0f] GeV: reff_pt = %.3f", pt, this_low_edge_pt, this_up_edge_pt, reff_pt ); }

    	        float reff_eta(1.0), reff_eta_err_up(0.0), reff_eta_err_dn(0.0);

    	        if ( m_useEtaParametrisation ) {

	    	    // Loop over number of eta bins
    	            // Do not consider underflow, i.e. 0th bin
    	            //
    	            for ( int e(1); e <= hist_eta->GetNbinsX()+1; ++e ) {

	    	  	this_low_edge_eta = hist_eta->GetXaxis()->GetBinLowEdge(e);
    	        	this_up_edge_eta  = hist_eta->GetXaxis()->GetBinLowEdge(e+1);

    	        	if ( m_verbose ) { Info("getMMEfficiencyAndError()","\t\t|eta| bin %i : [%.3f,%.3f]", e, this_low_edge_eta, this_up_edge_eta ); }

    	        	if ( fabs(eta) >= this_low_edge_eta && fabs(eta) < this_up_edge_eta ) {

		 	    if ( m_useTEfficiency ) {
		 		 reff_eta	 = teff_eta->GetEfficiency(e);
		 		 reff_eta_err_up = teff_eta->GetEfficiencyErrorUp(e);
		 		 reff_eta_err_dn = teff_eta->GetEfficiencyErrorLow(e);
		 	    } else {
		 		 reff_eta        = hist_eta->GetBinContent(e);
		 		 reff_eta_err_up = reff_eta_err_dn = hist_eta->GetBinError(e);
                 	    }

			    if ( m_verbose ) {
    	        		Info("getMMEfficiencyAndError()", "\t\tLepton |eta| = %.3f ==> Reading real efficiency in |eta| bin [%.3f,%.3f]: reff_eta = %.3f", fabs(eta), this_low_edge_eta, this_up_edge_eta, reff_eta );
    	        	    }

    	        	    break;
    	        	}
    	            }
    	        }

    	        // Nominal
    	        //
    	        efficiency.at(0) = reff_pt;
    	        error_up	 = reff_pt_err_up;
    	        error_dn	 = reff_pt_err_dn;

    	        // UP syst
    	        //
    	        efficiency.at(1) = ( reff_pt + error_up );

    	        // DN syst
    	        //
    	        if ( reff_pt - error_dn > 0 ) { efficiency.at(2) = ( reff_pt - error_dn ); }
    	        else			      { efficiency.at(2) = 0.0; }

    	        if ( m_useEtaParametrisation ) {

	    	    float reff_tot = ( lep.get()->flavour == 13 ) ? m_mu_reff_tot : m_el_reff_tot;
    	            if ( m_verbose ) { Info("getMMEfficiencyAndError()", "\t\t norm factor = %.3f", reff_tot ); }

	    	    efficiency.at(0) = ( reff_pt * reff_eta ) / reff_tot;

	    	    // Assuming  reff_pt,reff_eta are independent, this is the error on the product
    	            // ( the constant factor at denominator will be put back later in the def of Efficiency...)
    	            //
    	            error_up  = sqrt( (reff_eta*reff_pt_err_up)*(reff_eta*reff_pt_err_up) + (reff_pt*reff_eta_err_up)*(reff_pt*reff_eta_err_up) );
    	            error_dn  = sqrt( (reff_eta*reff_pt_err_dn)*(reff_eta*reff_pt_err_dn) + (reff_pt*reff_eta_err_dn)*(reff_pt*reff_eta_err_dn) );

    	            efficiency.at(1) = ( (reff_pt * reff_eta) + error_up ) / reff_tot;
    	            if ( (reff_pt * reff_eta) - error_dn > 0 ) { efficiency.at(2) = ( (reff_pt * reff_eta) - error_dn ) / reff_tot;}
    	            else				       { efficiency.at(2) = 0.0; }
    	        }

    	        break;
    	    }

    	} // close loop on pT bins: real case
    }

    if ( m_verbose ) {
        if ( type.compare("REAL") == 0 ) { Info("getMMEfficiencyAndError()", "\t\tEffective REAL efficiency ==> r = %.3f ( r_up = %.3f , r_dn = %.3f )", efficiency.at(0), efficiency.at(1), efficiency.at(2) ); }
        if ( type.compare("FAKE") == 0 ) { Info("getMMEfficiencyAndError()", "\t\tEffective FAKE efficiency ==> f = %.3f ( f_up = %.3f , f_dn = %.3f )", efficiency.at(0), efficiency.at(1), efficiency.at(2) ); }
    }

    return EL::StatusCode::SUCCESS;
}

EL::StatusCode HTopMultilepNTupReprocesser :: getMMWeightAndError( std::vector<float>& mm_weight,
								   const std::vector<float>& r0, const std::vector<float>& r1,
								   const std::vector<float>& f0, const std::vector<float>& f1 )
{

    if ( (r0.at(0) == 0) || (r1.at(0) == 0) || (r0.at(0) <= f0.at(0)) || (r1.at(0) <= f1.at(0)) ) {

    	if ( m_debug ) {
    	    Warning("getMMWeightAndError()", "Warning! The Matrix Method cannot be applied because : \nr0 = %.3f , r1 = %.3f, \nf0 = %.3f , f1 = %.3f", r0.at(0), r1.at(0),  f0.at(0), f1.at(0) );
    	    Warning("getMMWeightAndError()", "Setting MMWeight (nominal) = 0 ...");
    	}
        return EL::StatusCode::SUCCESS;

    } else {

	// Calculate nominal MM weight
    	//
    	mm_weight.at(0) = matrix_equation( f0.at(0), f1.at(0), r0.at(0), r1.at(0) );

    	// Calculate MM weight with systematics
    	//
    	float r0up = ( r0.at(1) > 1.0 ) ? 1.0 :  r0.at(1) ;
    	float r1up = ( r1.at(1) > 1.0 ) ? 1.0 :  r1.at(1) ;
    	float r0dn = r0.at(2);
    	float r1dn = r1.at(2);

    	float f0up = f0.at(1);
    	float f1up = f1.at(1);
    	float f0dn = ( f0.at(2) < 0.0 ) ? 0.0 :  f0.at(2) ;
    	float f1dn = ( f1.at(2) < 0.0 ) ? 0.0 :  f1.at(2) ;

    	// lep0, rup syst
    	//
    	mm_weight.at(1) = matrix_equation( f0.at(0), f1.at(0), r0up, r1.at(0) );
	
    	// lep0, rdn syst
    	//
    	if ( r0dn > f0.at(0) ) { mm_weight.at(2) = matrix_equation( f0.at(0), f1.at(0), r0dn, r1.at(0) ); }
        else { Warning("getMMWeightAndError()", "Warning! Systematic lep_0_rdn cannot be calculated because : \nr0dn = %.3f, \nf0 = %.3f", r0dn, f0.at(0)); }

    	// lep1, rup syst
    	//
    	mm_weight.at(3) = matrix_equation( f0.at(0), f1.at(0), r0.at(0), r1up );
	
    	// lep1, rdn syst
    	//
    	if ( r1dn > f1.at(0) ) { mm_weight.at(4) = matrix_equation( f0.at(0), f1.at(0), r0.at(0), r1dn ); }
        else { Warning("getMMWeightAndError()", "Warning! Systematic lep_1_rdn cannot be calculated because : \nr1dn = %.3f, \nf1 = %.3f", r1dn, f1.at(0) ); }

	// lep0, fup syst
    	//
       if ( r0.at(0) > f0up ) { mm_weight.at(5) = matrix_equation( f0up, f1.at(0), r0.at(0), r1.at(0) ); }
       else { Warning("getMMWeightAndError()", "Warning! Systematic lep_0_fup cannot be calculated because : \nf0up = %.3f, \nr0 = %.3f", f0up, r0.at(0)); }

	// lep0, fdn syst
    	//
    	mm_weight.at(6) = matrix_equation( f0dn, f1.at(0), r0.at(0), r1.at(0) );

	// lep1, fup syst
    	//
       if ( r1.at(0) > f1up ) { mm_weight.at(7) = matrix_equation( f0.at(0), f1up, r0.at(0), r1.at(0) ); }
       else { Warning("getMMWeightAndError()", "Warning! Systematic lep_1_fup cannot be calculated because : \nf1up = %.3f, \nr1 = %.3f", f1up, r1.at(0)); }

	// lep1, fdn syst
    	//
    	mm_weight.at(8) = matrix_equation( f0.at(0), f1dn, r0.at(0), r1.at(0) );

    }

    return EL::StatusCode::SUCCESS;

}

float HTopMultilepNTupReprocesser :: matrix_equation ( const float& f0, const float& f1, const float& r0, const float& r1 )
{

    float w      = 1.0;
    float alpha  = 1.0 / ( (r0-f0) * (r1-f1) );

    if ( m_event.get()->TT ) {
        if ( m_verbose ) { Info("matrix_equation()", "In region TT:"); }
        w = 1.0 - ( r0 * r1 * ( 1.0 -f0 ) * ( 1.0 - f1 ) * alpha );
    } else if ( m_event.get()->TAntiT ) {
        if ( m_verbose ) { Info("matrix_equation()", "In region TAntiT:"); }
        w = r0 * r1 * f1 * ( 1.0 - f0 ) * alpha;
    } else if ( m_event.get()->AntiTT ) {
        if ( m_verbose ) { Info("matrix_equation()", "In region AntiTT:"); }
        w = r0 * r1 * f0 * ( 1.0 - f1 ) * alpha;
    } else if ( m_event.get()->AntiTAntiT ) {
        if ( m_verbose ) { Info("matrix_equation()", "In region AntiTAntiT:"); }
        w = -1.0 * r0 * r1 * f0 * f1 * alpha;
    }

    if ( m_verbose ) { Info("matrix_equation()", "\nr0 = %.3f, r1 = %.3f, f0 = %.3f, f1 = %.3f\nw = %.3f , alpha = %.3f ", r0, r1, f0, f1, w, alpha); }

    // The above formulas are equivalent to the following:
    //
    //float w2 = 1.0;
    //if      ( m_event.get()->TT	   ) { w2 = alpha * ( r0 * f1 * ( (f0 - 1) * (1 - r1) ) + r1 * f0 * ( (r0 - 1) * (1 - f1) ) + f0 * f1 * ( (1 - r0) * (1 - r1) ) ); }
    //else if ( m_event.get()->TAntiT	   ) { w2 = alpha * ( r0 * f1 * ( (1 - f0) * r1 ) + r1 * f0 * ( (1 - r0) * f1 ) + f0 * f1 * ( (r0 - 1) * r1 ) ); }
    //else if ( m_event.get()->AntiTT	   ) { w2 = alpha * ( r0 * f1 * ( (1 - r1) * f0 ) + r1 * f0 * ( (1 - f1) * r0 ) + f0 * f1 * ( (r1 - 1) * r0 ) ); }
    //else if ( m_event.get()->AntiTAntiT  ) { w2 = alpha * ( r0 * f1 * ( -1.0 * f0 * r1 ) + r1 * f0 * ( -1.0 * r0 * f1 ) + f0 * f1 * ( r0 * r1 ) ); }

    return w;
}


// passs "SYS" as parameter to this method

// -) statistical unc
// -) QMisID numerator
// -) QMisId denominator
// ...

// pass "SYS" as parameter to getMMEfficiencyAndError()
// it will read the correct histogram  based on the bin lep0 and lep1 are found

// getMMWeightAndError will not change

// store the weights in a std::map belonging to m_event:

//  m_event.get()->weight_MM_lep0_UP["SYS"]

// is there a way to be smart when saving the branches to output, at all?

EL::StatusCode HTopMultilepNTupReprocesser :: calculateMMWeights()
{
    ANA_CHECK_SET_TYPE (EL::StatusCode);

    // If is not a dileptonic/trileptonic event, return
    //
    if ( m_dilep_type <= 0 && m_trilep_type <= 0 ) { return EL::StatusCode::SUCCESS; }

    std::shared_ptr<leptonObj> lep0 = m_leptons.at(0);
    std::shared_ptr<leptonObj> lep1 = m_leptons.at(1);

    // These are the "effective" r/f efficiencies for each lepton, obtained by reading the input r/f histogram(s)

    std::vector<float> r0 = { 1.0, 0.0, 0.0 };
    std::vector<float> r1 = { 1.0, 0.0, 0.0 };
    std::vector<float> f0 = { 1.0, 0.0, 0.0 };
    std::vector<float> f1 = { 1.0, 0.0, 0.0 };

    ANA_CHECK( this->getMMEfficiencyAndError( lep0, r0, "REAL" ) );
    ANA_CHECK( this->getMMEfficiencyAndError( lep1, r1, "REAL" ) );
    ANA_CHECK( this->getMMEfficiencyAndError( lep0, f0, "FAKE" ) );
    ANA_CHECK( this->getMMEfficiencyAndError( lep1, f1, "FAKE" ) );

    if ( m_debug ) {
        std::cout << "" << std::endl;
	Info("calculateMMWeights()", "Lepton 0 - effective real eff. (nominal, up, dn): " );
	for ( unsigned int idx(0); idx < r0.size(); ++idx ) { std::cout << "r0[" << idx << "] = " << std::setprecision(3) << r0.at(idx) << std::endl; }
	Info("calculateMMWeights()", "Lepton 1 - effective real eff. (nominal, up, dn): " );
	for ( unsigned int idx(0); idx < r1.size(); ++idx ) { std::cout << "r1[" << idx << "] = " << std::setprecision(3) << r1.at(idx) << std::endl; }
	Info("calculateMMWeights()", "Lepton 0 - effective fake eff. (nominal, up, dn): " );
	for ( unsigned int idx(0); idx < f0.size(); ++idx ) { std::cout << "f0[" << idx << "] = " << std::setprecision(3) << f0.at(idx) << std::endl; }
	Info("calculateMMWeights()", "Lepton 1 - effective fake eff. (nominal, up, dn): " );
	for ( unsigned int idx(0); idx < f1.size(); ++idx ) { std::cout << "f1[" << idx << "] = " << std::setprecision(3) << f1.at(idx) << std::endl; }
	std::cout << "" << std::endl;
    }

    std::vector<float> mm_weight = { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };

    ANA_CHECK( this->getMMWeightAndError( mm_weight, r0, r1, f0, f1 ) );

    // For variations, save relative weight wrt. nominal

    m_event.get()->weight_MM = mm_weight.at(0);
    m_event.get()->weight_MM_lep0_R_stat_UP = ( !std::isnan(mm_weight.at(1)/mm_weight.at(0)) && !std::isinf(mm_weight.at(1)/mm_weight.at(0)) ) ? mm_weight.at(1)/mm_weight.at(0) : 0.0;
    m_event.get()->weight_MM_lep0_R_stat_DN = ( !std::isnan(mm_weight.at(2)/mm_weight.at(0)) && !std::isinf(mm_weight.at(2)/mm_weight.at(0)) ) ? mm_weight.at(2)/mm_weight.at(0) : 0.0;
    m_event.get()->weight_MM_lep1_R_stat_UP = ( !std::isnan(mm_weight.at(3)/mm_weight.at(0)) && !std::isinf(mm_weight.at(3)/mm_weight.at(0)) ) ? mm_weight.at(3)/mm_weight.at(0) : 0.0;
    m_event.get()->weight_MM_lep1_R_stat_DN = ( !std::isnan(mm_weight.at(4)/mm_weight.at(0)) && !std::isinf(mm_weight.at(4)/mm_weight.at(0)) ) ? mm_weight.at(4)/mm_weight.at(0) : 0.0;
    m_event.get()->weight_MM_lep0_F_stat_UP = ( !std::isnan(mm_weight.at(5)/mm_weight.at(0)) && !std::isinf(mm_weight.at(5)/mm_weight.at(0)) ) ? mm_weight.at(5)/mm_weight.at(0) : 0.0;
    m_event.get()->weight_MM_lep0_F_stat_DN = ( !std::isnan(mm_weight.at(6)/mm_weight.at(0)) && !std::isinf(mm_weight.at(6)/mm_weight.at(0)) ) ? mm_weight.at(6)/mm_weight.at(0) : 0.0;
    m_event.get()->weight_MM_lep1_F_stat_UP = ( !std::isnan(mm_weight.at(7)/mm_weight.at(0)) && !std::isinf(mm_weight.at(7)/mm_weight.at(0)) ) ? mm_weight.at(7)/mm_weight.at(0) : 0.0;
    m_event.get()->weight_MM_lep1_F_stat_DN = ( !std::isnan(mm_weight.at(8)/mm_weight.at(0)) && !std::isinf(mm_weight.at(8)/mm_weight.at(0)) ) ? mm_weight.at(8)/mm_weight.at(0) : 0.0;

    return EL::StatusCode::SUCCESS;
}
