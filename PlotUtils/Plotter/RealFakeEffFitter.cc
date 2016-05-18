/**
 * @file   RealFakeEffFitter.cc
 * @author Marco Milesi <marco.milesi@cern.ch>
 * @date   10 March 2016
 * @brief  ROOT macro to measure real/fake efficiencies via a binned maximum likelihood fit.
 *
 * Use ROOT::TMinuit class
 * @see https://root.cern.ch/doc/master/classTMinuit.html
 *
 */

#include <TROOT.h>
#include "TSystem.h"
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <tuple>
#include "TMath.h"
#include "TFile.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TMinuit.h"
#include "TGraphErrors.h"
#include "TLatex.h"
#include "TEfficiency.h"
#include "TGraphAsymmErrors.h"
#include "AtlasStyle.C"
#include "TLine.h"

// -------------------------------------------------------------------------------------

// GLOBAL VARIABLES, FUNCTIONS (TMinuit fiited function must be global, unfortunately...)

bool g_verbose(false);

int g_nPtBins_Squared;

/**
  Estimated parameters' indexes
  These vectors contain the corresponding index in the total par[] vector of the TMinuit object
  --> can use these quantities in the likelihood function!
*/
std::vector<int> g_rel_idxs;
std::vector<int> g_fel_idxs;
std::vector<int> g_rmu_idxs;
std::vector<int> g_fmu_idxs;

std::vector<int> g_RelRel_idxs;
std::vector<int> g_FelRel_idxs;
std::vector<int> g_RelFel_idxs;
//std::vector<int> g_FelFel_idxs;
std::vector<int> g_RmuRmu_idxs;
std::vector<int> g_FmuRmu_idxs;
std::vector<int> g_RmuFmu_idxs;
//std::vector<int> g_FmuFmu_idxs;
std::vector<int> g_RelRmu_idxs;
std::vector<int> g_FelRmu_idxs;
std::vector<int> g_RelFmu_idxs;
//std::vector<int> g_FelFmu_idxs;
std::vector<int> g_RmuRel_idxs;
std::vector<int> g_FmuRel_idxs;
std::vector<int> g_RmuFel_idxs;
//std::vector<int> g_FmuFel_idxs;

std::vector<int> g_r1el_idxs;  // x-coordinate  (--> leading pT axis) of the leading lepton in the (x_i,y_j) bin
std::vector<int> g_r2el_idxs;  // y-coordinate  (--> subleading pT axis) of the subleading lepton in the (x_i,y_j) bin
std::vector<int> g_f1el_idxs;  // x-coordinate  (--> leading pT axis) of the leading lepton in the (x_i,y_j) bin
std::vector<int> g_f2el_idxs;  // y-coordinate  (--> subleading pT axis) of the subleading lepton in the (x_i,y_j) bin};
std::vector<int> g_r1mu_idxs;  // x-coordinate  (--> leading pT axis) of the leading lepton in the (x_i,y_j) bin
std::vector<int> g_r2mu_idxs;  // y-coordinate  (--> subleading pT axis) of the subleading lepton in the (x_i,y_j) bin
std::vector<int> g_f1mu_idxs;  // x-coordinate  (--> leading pT axis) of the leading lepton in the (x_i,y_j) bin
std::vector<int> g_f2mu_idxs;  // y-coordinate  (--> subleading pT axis) of the subleading lepton in the (x_i,y_j) bin};

std::vector<double> g_fitted_r1_el; // fitted r value for leading e in every 2D bin
std::vector<double> g_fitted_r2_el; // fitted r value for subleading e in every 2D bin
std::vector<double> g_fitted_r1_mu; // fitted r value for leading mu in every 2D bin
std::vector<double> g_fitted_r2_mu; // fitted r value for subleading mu in every 2D bin

std::vector<double> g_TelTel_resized;
std::vector<double> g_TelLel_resized;
std::vector<double> g_LelTel_resized;
std::vector<double> g_LelLel_resized;

std::vector<double> g_TmuTmu_resized;
std::vector<double> g_TmuLmu_resized;
std::vector<double> g_LmuTmu_resized;
std::vector<double> g_LmuLmu_resized;

std::vector<double> g_TelTmu_resized;
std::vector<double> g_TelLmu_resized;
std::vector<double> g_LelTmu_resized;
std::vector<double> g_LelLmu_resized;

std::vector<double> g_TmuTel_resized;
std::vector<double> g_TmuLel_resized;
std::vector<double> g_LmuTel_resized;
std::vector<double> g_LmuLel_resized;

bool g_elec(false);
bool g_muon(false);
bool g_incl(false);

bool g_reff(false);
bool g_feff(false);
bool g_RR(false);
bool g_RF(false);
bool g_FR(false);
//bool g_FF(false);

/**
  Define global likelihood function to be minimised
*/
void myLikelihood( int& nDim, double* gout, double& result, double par[], int flg ) {

   if ( g_verbose ) { std::cout << "" << std::endl; }

   double likelihood_TelTel(0.0), likelihood_TelLel(0.0), likelihood_LelTel(0.0), likelihood_LelLel(0.0);
   double likelihood_TmuTmu(0.0), likelihood_TmuLmu(0.0), likelihood_LmuTmu(0.0), likelihood_LmuLmu(0.0);
   double likelihood_TelTmu(0.0), likelihood_TelLmu(0.0), likelihood_LelTmu(0.0), likelihood_LelLmu(0.0);
   double likelihood_TmuTel(0.0), likelihood_TmuLel(0.0), likelihood_LmuTel(0.0), likelihood_LmuLel(0.0);

   double likelihood_TT(0.0), likelihood_TL(0.0), likelihood_LT(0.0), likelihood_LL(0.0);

   double likelihood(0.0);

   double obs_TelTel(-1.0), obs_TelLel(-1.0), obs_LelTel(-1.0), obs_LelLel(-1.0);
   double obs_TmuTmu(-1.0), obs_TmuLmu(-1.0), obs_LmuTmu(-1.0), obs_LmuLmu(-1.0);
   double obs_TelTmu(-1.0), obs_TelLmu(-1.0), obs_LelTmu(-1.0), obs_LelLmu(-1.0);
   double obs_TmuTel(-1.0), obs_TmuLel(-1.0), obs_LmuTel(-1.0), obs_LmuLel(-1.0);

   double exp_TelTel(-1.0), exp_TelLel(-1.0), exp_LelTel(-1.0), exp_LelLel(-1.0);
   double exp_TmuTmu(-1.0), exp_TmuLmu(-1.0), exp_LmuTmu(-1.0), exp_LmuLmu(-1.0);
   double exp_TelTmu(-1.0), exp_TelLmu(-1.0), exp_LelTmu(-1.0), exp_LelLmu(-1.0);
   double exp_TmuTel(-1.0), exp_TmuLel(-1.0), exp_LmuTel(-1.0), exp_LmuLel(-1.0);

   double r1el(0.0), r2el(0.0), f1el(0.0), f2el(0.0);
   double r1mu(0.0), r2mu(0.0), f1mu(0.0), f2mu(0.0);

   double RelRel(0.0), RelFel(0.0), FelRel(0.0), FelFel(0.0);
   double RmuRmu(0.0), RmuFmu(0.0), FmuRmu(0.0), FmuFmu(0.0);
   double RelRmu(0.0), RelFmu(0.0), FelRmu(0.0), FelFmu(0.0);
   double RmuRel(0.0), RmuFel(0.0), FmuRel(0.0), FmuFel(0.0);

   // Compute the likelihood by summing TL,LT.. sub-blocks in every bin of the (linearised) 2D pT histogram
   //
   for ( int ibin = 0; ibin < g_nPtBins_Squared; ++ibin  ) {

     // Read the likelihood parameters from the TMinuit par[] vector
     //

     // This assumes real efficiencies are fitted first
     // When fitting fake efficiencies, the previously fitted values for r are used

     double fitted_r1el(0.0), fitted_r2el(0.0);
     double fitted_r1mu(0.0), fitted_r2mu(0.0);
     if (  g_feff && ( g_elec || g_incl ) ) { fitted_r1el = g_fitted_r1_el.at(ibin); fitted_r2el = g_fitted_r2_el.at(ibin); }
     if (  g_feff && ( g_muon || g_incl ) ) { fitted_r1mu = g_fitted_r1_mu.at(ibin); fitted_r2mu = g_fitted_r2_mu.at(ibin); }

     r1el = ( g_reff && ( g_elec || g_incl ) )  ? par[ g_r1el_idxs.at(ibin) ] : fitted_r1el;
     r2el = ( g_reff && ( g_elec || g_incl ) )  ? par[ g_r2el_idxs.at(ibin) ] : fitted_r2el;
     f1el = ( g_feff && ( g_elec || g_incl ) )  ? par[ g_f1el_idxs.at(ibin) ] : 0.0;
     f2el = ( g_feff && ( g_elec || g_incl ) )  ? par[ g_f2el_idxs.at(ibin) ] : 0.0;
     r1mu = ( g_reff && ( g_muon || g_incl ) )  ? par[ g_r1mu_idxs.at(ibin) ] : fitted_r1mu;
     r2mu = ( g_reff && ( g_muon || g_incl ) )  ? par[ g_r2mu_idxs.at(ibin) ] : fitted_r2mu;
     f1mu = ( g_feff && ( g_muon || g_incl ) )  ? par[ g_f1mu_idxs.at(ibin) ] : 0.0;
     f2mu = ( g_feff && ( g_muon || g_incl ) )  ? par[ g_f2mu_idxs.at(ibin) ] : 0.0;
     RelRel = (  g_RR && ( g_elec || g_incl ) )  ? par[ g_RelRel_idxs.at(ibin) ] : 0.0;
     RelFel = (  g_RF && ( g_elec || g_incl ) )  ? par[ g_RelFel_idxs.at(ibin) ] : 0.0;
     FelRel = (  g_FR && ( g_elec || g_incl ) )  ? par[ g_FelRel_idxs.at(ibin) ] : 0.0;
     //FelFel = (  g_FF && ( g_elec || g_incl ) )  ? par[ g_FelFel_idxs.at(ibin) ] : 0.0; // can we set this to 0 by brute force?
     FelFel = 0.0;
     RmuRmu = (  g_RR && ( g_muon || g_incl ) )  ? par[ g_RmuRmu_idxs.at(ibin) ] : 0.0;
     RmuFmu = (  g_RF && ( g_muon || g_incl ) )  ? par[ g_RmuFmu_idxs.at(ibin) ] : 0.0;
     FmuRmu = (  g_FR && ( g_muon || g_incl ) )  ? par[ g_FmuRmu_idxs.at(ibin) ] : 0.0;
     //FmuFmu = (  g_FF && ( g_muon || g_incl ) )  ? par[ g_FmuFmu_idxs.at(ibin) ] : 0.0; // can we set this to 0 by brute force?
     FmuFmu = 0.0;
     RmuRel = (  g_RR && g_incl )  ? par[ g_RmuRel_idxs.at(ibin) ] : 0.0;
     RmuFel = (  g_RF && g_incl )  ? par[ g_RmuFel_idxs.at(ibin) ] : 0.0;
     FmuRel = (  g_FR && g_incl )  ? par[ g_FmuRel_idxs.at(ibin) ] : 0.0;
     //FmuFel = (  g_FF && g_incl )  ? par[ g_FmuFel_idxs.at(ibin) ] : 0.0; // can we set this to 0 by brute force?
     FmuFel = 0.0;
     RelRmu = (  g_RR && g_incl )  ? par[ g_RelRmu_idxs.at(ibin) ] : 0.0;
     RelFmu = (  g_RF && g_incl )  ? par[ g_RelFmu_idxs.at(ibin) ] : 0.0;
     FelRmu = (  g_FR && g_incl )  ? par[ g_FelRmu_idxs.at(ibin) ] : 0.0;
     //FelFmu = (  g_FF && g_incl )  ? par[ g_FelFmu_idxs.at(ibin) ] : 0.0; // can we set this to 0 by brute force?
     FelFmu = 0.0;


     if ( g_verbose ) {
       std::cout << "" << std::endl;
       Info("myLikelihood()","Ingredients of likelihood - global bin (%i):", ibin );
       std::cout << "\tr1el = " << r1el << std::endl;
       std::cout << "\tr2el = " << r2el << std::endl;
       std::cout << "\tf1el = " << f1el << std::endl;
       std::cout << "\tf2el = " << f2el << std::endl;
       std::cout << "\tr1mu = " << r1mu << std::endl;
       std::cout << "\tr2mu = " << r2mu << std::endl;
       std::cout << "\tf1mu = " << f1mu << std::endl;
       std::cout << "\tf2mu = " << f2mu << std::endl;
       std::cout << "\tRelRel = " << RelRel << std::endl;
       std::cout << "\tRelFel = " << RelFel << std::endl;
       std::cout << "\tFelRel = " << FelRel << std::endl;
       std::cout << "\tFelFel = " << FelFel << std::endl;
       std::cout << "\tRmuRmu = " << RmuRmu << std::endl;
       std::cout << "\tRmuFmu = " << RmuFmu << std::endl;
       std::cout << "\tFmuRmu = " << FmuRmu << std::endl;
       std::cout << "\tFmuFmu = " << FmuFmu << std::endl;
       std::cout << "\tRmuRel = " << RmuRel << std::endl;
       std::cout << "\tRmuFel = " << RmuFel << std::endl;
       std::cout << "\tFmuRel = " << FmuRel << std::endl;
       std::cout << "\tFmuFel = " << FmuFel << std::endl;
       std::cout << "\tRelRmu = " << RelRmu << std::endl;
       std::cout << "\tRelFmu = " << RelFmu << std::endl;
       std::cout << "\tFelRmu = " << FelRmu << std::endl;
       std::cout << "\tFelFmu = " << FelFmu << std::endl;
       std::cout << "" << std::endl;
     }

     // TT block
     //
     obs_TelTel  = g_TelTel_resized.at(ibin);
     exp_TelTel  = r1el * r2el * RelRel + r1el * f2el * RelFel + r2el * f1el * FelRel + f1el * f2el * FelFel;
     if ( g_verbose ) {
       std::cout << "" << std::endl;
       Info("myLikelihood()","Adding term in likelihood for observed selection: TelTel in global bin (%i)", ibin );
       std::cout << "\tobs_TelTel = " << obs_TelTel << " - exp_TelTel = " << exp_TelTel << " - likelihood block = " << ( obs_TelTel * log( exp_TelTel ) - ( exp_TelTel ) ) << std::endl;
       std::cout << "" << std::endl;
     }
     likelihood_TelTel = ( obs_TelTel * log( exp_TelTel ) - ( exp_TelTel ) );

     obs_TmuTmu  = g_TmuTmu_resized.at(ibin);
     exp_TmuTmu  = r1mu * r2mu * RmuRmu + r1mu * f2mu * RmuFmu + r2mu * f1mu * FmuRmu + f1mu * f2mu * FmuFmu;
     if ( g_verbose ) {
       std::cout << "" << std::endl;
       Info("myLikelihood()","Adding term in likelihood for observed selection: TmuTmu in global bin (%i)", ibin );
       std::cout << "\tobs_TmuTmu = " << obs_TmuTmu << " - exp_TmuTmu = " << exp_TmuTmu << " - likelihood block = " << ( obs_TmuTmu * log( exp_TmuTmu ) - ( exp_TmuTmu ) ) << std::endl;
       std::cout << "" << std::endl;
     }
     likelihood_TmuTmu = ( obs_TmuTmu * log( exp_TmuTmu ) - ( exp_TmuTmu ) );

     obs_TmuTel  = g_TmuTel_resized.at(ibin);
     exp_TmuTel  = r1mu * r2el * RmuRel + r1mu * f2el * RmuFel + r2el * f1mu * FmuRel + f1mu * f2el * FmuFel;
     if ( g_verbose ) {
       std::cout << "" << std::endl;
       Info("myLikelihood()","Adding term in likelihood for observed selection: TmuTel in global bin (%i)", ibin );
       std::cout << "\tobs_TmuTel = " << obs_TmuTel << " - exp_TmuTel = " << exp_TmuTel << " - likelihood block = " << ( obs_TmuTel * log( exp_TmuTel ) - ( exp_TmuTel ) ) << std::endl;
       std::cout << "" << std::endl;
     }
     likelihood_TmuTel = ( obs_TmuTel * log( exp_TmuTel ) - ( exp_TmuTel ) );

     obs_TelTmu  = g_TelTmu_resized.at(ibin);
     exp_TelTmu  = r1el * r2mu * RelRmu + r1el * f2mu * RelFmu + r2mu * f1el * FelRmu + f1el * f2mu * FelFmu;
     if ( g_verbose ) {
       std::cout << "" << std::endl;
       Info("myLikelihood()","Adding term in likelihood for observed selection: TelTmu in global bin (%i)", ibin );
       std::cout << "\tobs_TelTmu = " << obs_TelTmu << " - exp_TelTmu = " << exp_TelTmu << " - likelihood block = " << ( obs_TelTmu * log( exp_TelTmu ) - ( exp_TelTmu ) ) << std::endl;
       std::cout << "" << std::endl;
     }
     likelihood_TelTmu = ( obs_TelTmu * log( exp_TelTmu ) - ( exp_TelTmu ) );

     likelihood_TT = likelihood_TelTel + likelihood_TmuTmu + likelihood_TmuTel + likelihood_TelTmu;

     // TL block
     //
     obs_TelLel  = g_TelLel_resized.at(ibin);
     exp_TelLel  = r1el * ( 1 - r2el ) * RelRel + r1el * ( 1 - f2el ) * RelFel + f1el * ( 1 - r2el ) * FelRel + f1el * ( 1 - f2el ) * FelFel;
     if ( g_verbose ) {
       std::cout << "" << std::endl;
       Info("myLikelihood()","Adding term in likelihood for observed selection: TelLel in global bin (%i)", ibin );
       std::cout << "\tobs_TelLel = " << obs_TelLel << " - exp_TelLel = " << exp_TelLel << " - likelihood block = " << ( obs_TelLel * log( exp_TelLel ) - ( exp_TelLel ) ) << std::endl;
       std::cout << "" << std::endl;
     }
     likelihood_TelLel = ( obs_TelLel * log( exp_TelLel ) - ( exp_TelLel ) );

     obs_TmuLmu  = g_TmuLmu_resized.at(ibin);
     exp_TmuLmu  = r1mu * ( 1 - r2mu ) * RmuRmu + r1mu * ( 1 - f2mu ) * RmuFmu + f1mu * ( 1 - r2mu ) * FmuRmu + f1mu * ( 1 - f2mu ) * FmuFmu;
     if ( g_verbose ) {
       std::cout << "" << std::endl;
       Info("myLikelihood()","Adding term in likelihood for observed selection: TmuLmu in global bin (%i)", ibin );
       std::cout << "\tobs_TmuLmu = " << obs_TmuLmu << " - exp_TmuLmu = " << exp_TmuLmu << " - likelihood block = " << ( obs_TmuLmu * log( exp_TmuLmu ) - ( exp_TmuLmu ) ) << std::endl;
       std::cout << "" << std::endl;
     }
     likelihood_TmuLmu = ( obs_TmuLmu * log( exp_TmuLmu ) - ( exp_TmuLmu ) );

     obs_TmuLel  = g_TmuLel_resized.at(ibin);
     exp_TmuLel  = r1mu * ( 1 - r2el ) * RmuRel + r1mu * ( 1 - f2el ) * RmuFel + f1mu * ( 1 - r2el ) * FmuRel + f1mu * ( 1 - f2el ) * FmuFel;
     if ( g_verbose ) {
       std::cout << "" << std::endl;
       Info("myLikelihood()","Adding term in likelihood for observed selection: TmuLel in global bin (%i)", ibin );
       std::cout << "\tobs_TmuLel = " << obs_TmuLel << " - exp_TmuLel = " << exp_TmuLel << " - likelihood block = " << ( obs_TmuLel * log( exp_TmuLel ) - ( exp_TmuLel ) ) << std::endl;
       std::cout << "" << std::endl;
     }
     likelihood_TmuLel = ( obs_TmuLel * log( exp_TmuLel ) - ( exp_TmuLel ) );

     obs_TelLmu  = g_TelLmu_resized.at(ibin);
     exp_TelLmu  = r1el * ( 1 - r2mu ) * RelRmu + r1el * ( 1 - f2mu ) * RelFmu + f1el * ( 1 - r2mu ) * FelRmu + f1el * ( 1 - f2mu ) * FelFmu;
     if ( g_verbose ) {
       std::cout << "" << std::endl;
       Info("myLikelihood()","Adding term in likelihood for observed selection: TelLmu in global bin (%i)", ibin );
       std::cout << "\tobs_TelLmu = " << obs_TelLmu << " - exp_TelLmu = " << exp_TelLmu << " - likelihood block = " << ( obs_TelLmu * log( exp_TelLmu ) - ( exp_TelLmu ) ) << std::endl;
       std::cout << "" << std::endl;
     }
     likelihood_TelLmu = ( obs_TelLmu * log( exp_TelLmu ) - ( exp_TelLmu ) );

     likelihood_TL = likelihood_TelLel + likelihood_TmuLmu + likelihood_TmuLel + likelihood_TelLmu;

     // LT block
     //
     obs_LelTel  = g_LelTel_resized.at(ibin);
     exp_LelTel  = r2el * ( 1 - r1el ) * RelRel + f2el * ( 1 - r1el ) * RelFel + r2el * ( 1 - f1el ) * FelRel + f2el * ( 1 - f1el ) * FelFel;
     if ( g_verbose ) {
       std::cout << "" << std::endl;
       Info("myLikelihood()","Adding term in likelihood for observed selection: LelTel in global bin (%i)", ibin );
       std::cout << "\tobs_LelTel = " << obs_LelTel << " - exp_LelTel = " << exp_LelTel << " - likelihood block = " << ( obs_LelTel * log( exp_LelTel ) - ( exp_LelTel ) ) << std::endl;
       std::cout << "" << std::endl;
     }
     likelihood_LelTel = ( obs_LelTel * log( exp_LelTel ) - ( exp_LelTel ) );

     obs_LmuTmu  = g_LmuTmu_resized.at(ibin);
     exp_LmuTmu  = r2mu * ( 1 - r1mu ) * RmuRmu + f2mu * ( 1 - r1mu ) * RmuFmu + r2mu * ( 1 - f1mu ) * FmuRmu + f2mu * ( 1 - f1mu ) * FmuFmu;
     if ( g_verbose ) {
       std::cout << "" << std::endl;
       Info("myLikelihood()","Adding term in likelihood for observed selection: LmuTmu in global bin (%i)", ibin );
       std::cout << "\tobs_LmuTmu = " << obs_LmuTmu << " - exp_LmuTmu = " << exp_LmuTmu << " - likelihood block = " << ( obs_LmuTmu * log( exp_LmuTmu ) - ( exp_LmuTmu ) ) << std::endl;
       std::cout << "" << std::endl;
     }
     likelihood_LmuTmu = ( obs_LmuTmu * log( exp_LmuTmu ) - ( exp_LmuTmu ) );

     obs_LmuTel  = g_LmuTel_resized.at(ibin);
     exp_LmuTel  = r2el * ( 1 - r1mu ) * RmuRel + f2el * ( 1 - r1mu ) * RmuFel + r2el * ( 1 - f1mu ) * FmuRel + f2el * ( 1 - f1mu ) * FmuFel;
     if ( g_verbose ) {
       std::cout << "" << std::endl;
       Info("myLikelihood()","Adding term in likelihood for observed selection: LmuTel in global bin (%i)", ibin );
       std::cout << "\tobs_LmuTel = " << obs_LmuTel << " - exp_LmuTel = " << exp_LmuTel << " - likelihood block = " << ( obs_LmuTel * log( exp_LmuTel ) - ( exp_LmuTel ) ) << std::endl;
       std::cout << "" << std::endl;
     }
     likelihood_LmuTel = ( obs_LmuTel * log( exp_LmuTel ) - ( exp_LmuTel ) );

     obs_LelTmu  = g_LelTmu_resized.at(ibin);
     exp_LelTmu  = r2mu * ( 1 - r1el ) * RelRmu + f2mu * ( 1 - r1el ) * RelFmu + r2mu * ( 1 - f1el ) * FelRmu + f2mu * ( 1 - f1el ) * FelFmu;
     if ( g_verbose ) {
       std::cout << "" << std::endl;
       Info("myLikelihood()","Adding term in likelihood for observed selection: LelTmu in global bin (%i)", ibin );
       std::cout << "\tobs_LelTmu = " << obs_LelTmu << " - exp_LelTmu = " << exp_LelTmu << " - likelihood block = " << ( obs_LelTmu * log( exp_LelTmu ) - ( exp_LelTmu ) ) << std::endl;
       std::cout << "" << std::endl;
     }
     likelihood_LelTmu = ( obs_LelTmu * log( exp_LelTmu ) - ( exp_LelTmu ) );

     likelihood_LT = likelihood_LelTel + likelihood_LmuTmu + likelihood_LmuTel + likelihood_LelTmu;

     // LL block
     //
     obs_LelLel  = g_LelLel_resized.at(ibin);
     exp_LelLel  = ( 1 - r1el ) * ( 1 - r2el ) * RelRel + ( 1 - r1el ) * ( 1 - f2el ) * RelFel + ( 1 - f1el ) * ( 1 - r2el ) * FelRel + ( 1 - f1el ) * ( 1 - f2el ) * FelFel;
     if ( g_verbose ) {
       std::cout << "" << std::endl;
       Info("myLikelihood()","Adding term in likelihood for observed selection: LelLel in global bin (%i)", ibin );
       std::cout << "\tobs_LelLel = " << obs_LelLel << " - exp_LelLel = " << exp_LelLel << " - likelihood block = " << ( obs_LelLel * log( exp_LelLel ) - ( exp_LelLel ) ) << std::endl;
       std::cout << "" << std::endl;
     }
     likelihood_LelLel = ( obs_LelLel * log( exp_LelLel ) - ( exp_LelLel ) );

     obs_LmuLmu  = g_LmuLmu_resized.at(ibin);
     exp_LmuLmu  = ( 1 - r1mu ) * ( 1 - r2mu ) * RmuRmu + ( 1 - r1mu ) * ( 1 - f2mu ) * RmuFmu + ( 1 - f1mu ) * ( 1 - r2mu ) * FmuRmu + ( 1 - f1mu ) * ( 1 - f2mu ) * FmuFmu;
     if ( g_verbose ) {
       std::cout << "" << std::endl;
       Info("myLikelihood()","Adding term in likelihood for observed selection: LmuLmu in global bin (%i)", ibin );
       std::cout << "\tobs_LmuLmu = " << obs_LmuLmu << " - exp_LmuLmu = " << exp_LmuLmu << " - likelihood block = " << ( obs_LmuLmu * log( exp_LmuLmu ) - ( exp_LmuLmu ) ) << std::endl;
       std::cout << "" << std::endl;
     }
     likelihood_LmuLmu = ( obs_LmuLmu * log( exp_LmuLmu ) - ( exp_LmuLmu ) );

     obs_LmuLel  = g_LmuLel_resized.at(ibin);
     exp_LmuLel  = ( 1 - r1mu ) * ( 1 - r2el ) * RmuRel + ( 1 - r1mu ) * ( 1 - f2el ) * RmuFel + ( 1 - f1mu ) * ( 1 - r2el ) * FmuRel + ( 1 - f1mu ) * ( 1 - f2el ) * FmuFel;
     if ( g_verbose ) {
       std::cout << "" << std::endl;
       Info("myLikelihood()","Adding term in likelihood for observed selection: LmuLel in global bin (%i)", ibin );
       std::cout << "\tobs_LmuLel = " << obs_LmuLel << " - exp_LmuLel = " << exp_LmuLel << " - likelihood block = " << ( obs_LmuLel * log( exp_LmuLel ) - ( exp_LmuLel ) ) << std::endl;
       std::cout << "" << std::endl;
     }
     likelihood_LmuLel = ( obs_LmuLel * log( exp_LmuLel ) - ( exp_LmuLel ) );

     obs_LelLmu  = g_LelLmu_resized.at(ibin);
     exp_LelLmu  = ( 1 - r1el ) * ( 1 - r2mu ) * RelRmu + ( 1 - r1el ) * ( 1 - f2mu ) * RelFmu + ( 1 - f1el ) * ( 1 - r2mu ) * FelRmu + ( 1 - f1el ) * ( 1 - f2mu ) * FelFmu;
     if ( g_verbose ) {
       std::cout << "" << std::endl;
       Info("myLikelihood()","Adding term in likelihood for observed selection: LelLmu in global bin (%i)", ibin );
       std::cout << "\tobs_LelLmu = " << obs_LelLmu << " - exp_LelLmu = " << exp_LelLmu << " - likelihood block = " << ( obs_LelLmu * log( exp_LelLmu ) - ( exp_LelLmu ) ) << std::endl;
       std::cout << "" << std::endl;
     }
     likelihood_LelLmu = ( obs_LelLmu * log( exp_LelLmu ) - ( exp_LelLmu ) );

     likelihood_LL = likelihood_LelLel + likelihood_LmuLmu + likelihood_LmuLel + likelihood_LelLmu;

     // -------------------------------------------------------------------------

     if ( g_verbose ) { Info("myLikelihood()","Total likelihood block L(%i) = %2f.", ibin, ( likelihood_TT + likelihood_TL + likelihood_LT + likelihood_LL ) ); }

     likelihood += ( likelihood_TT + likelihood_TL + likelihood_LT + likelihood_LL );
   }

   if ( g_verbose ) { Info("myLikelihood()","===> Final likelihood - 2 * log(L) = %2f.", - 2.0 * likelihood ); }

   result = - 2.0 * likelihood;
}

/**
  Function to get histograms from file
*/
template<typename T>
T* get_object( TFile& file, const std::string& name ) {
    T* obj = dynamic_cast<T*>( file.Get(name.c_str()) );
    if ( !obj ) { throw std::runtime_error("object " + name + " not found"); }
    return obj;
}

/**
  Function to print content of a container
*/
template<typename T>
void printContainer( T& container, const std::string& message ) {
  std::cout << "" << std::endl;
  Info("printContainer()","%s",message.c_str() );
  unsigned int idx(0);
  for ( const auto& itr : container ) {
     std::cout << "\t[" << idx << "] = " << itr << std::endl;
     ++idx;
  }
  std::cout << "" << std::endl;
}

/**
  Function to print content of a container of errors
*/
void printErrorContainer( std::vector<std::tuple<double,double,double> >& container, const std::string& message ) {
  std::cout << "" << std::endl;
  Info("printErrorContainer()","%s",message.c_str() );
  unsigned int idx(0);
  for ( const auto& itr : container ) {
     std::cout << "\t[" << idx << "] - err UP = " << std::get<0>(itr) << " err DN = " << std::get<1>(itr) << " err CENT = " << std::get<2>(itr) << std::endl;
     ++idx;
  }
  std::cout << "" << std::endl;
}

// -------------------------------------------------------------------------------------

/**
  The main class for the fit
*/
class LHFitter {

  public :

    bool m_doSubtraction;
    bool m_doRebinning;

    enum kFlavour {
      ELEC  = 0,
      MUON  = 1,
      INCLUSIVE = 2,
    };

    enum kEfficiency {
      REAL  = 0,
      FAKE  = 1,
    };

    enum kVerbosity {
      NONE    = 0,
      DEBUG   = 1,
      VERBOSE = 2,
    };

    /**
      Class constructor:
      Set the type of efficiency to be fit, and the lepton flavour
    */
    LHFitter( kFlavour FLAVOUR, kEfficiency EFFICIENCY );

    /**
      Class destructor:
    */
    ~LHFitter();

    /**
      -) Read the yields for TT, TL, LT, LL, depending on the flavour and efficiency to be fit
      -) Reserve memory for parameters' vectors
      -) Set initial guesses for parameters r, f, RR, RF, FR, FF
      -) Create the TMinuit object and set NPAR, depending on initialisation
      -) Set the array of parameters for the fit (NB: every time this method gets called, the global parameters will be reset!)
    */
    void initialise();

    /**
      -) Calls MIGRAD and MINOS to perform the fit
      -) Save the fitted parameters into vectors
    */
    void fit();

    /**
      Set path for tag and probe files
    */
    inline void setTagAndProbePath( const std::string& path ) { m_input_path_TP = path; };

    /**
      Set path for input files with TL, LT... yields
    */
    inline void setInputHistPath( const std::string& path ) { m_input_path_yields = path; };

    inline void setVerbosity( kVerbosity VERBOSITY ) {
	if ( VERBOSITY == kVerbosity::DEBUG )   { m_debug = true; }
	if ( VERBOSITY == kVerbosity::VERBOSE ) { m_debug = true; m_verbose = true; }
    };

    /**
      Function to set bin grouping when rebinning w/ fixed bin size
    */
    inline void setBinGrouping( const int& groupsize ) {  m_nBinGroup = groupsize; };

    /**
      Function to set variable bins when rebinning w/ variable bin size
    */
    inline void setVariableBins( double *varbins, const int& nvarbins ) {
      m_useVariableBins = true;
      m_newNBins = nvarbins;
      m_newBins  = new double[m_newNBins+1];
      for ( int ibin(0); ibin < m_newNBins+1; ++ibin ) {
	  m_newBins[ibin] = varbins[ibin];
      }
    };

  private :

    /**
      Upper/lower limits for fit parameters and step size
      Declared static so they can be initialised once and for all
    */
    static double s_step_eff;
    static double s_up_eff;
    static double s_dn_eff;
    static double s_step_yields;
    static double s_up_yields;
    static double s_dn_yields;

    kFlavour    m_flavour;
    kEfficiency m_efficiency;

    std::string m_flavour_str;
    std::string m_efficiency_str;

    int     m_nBinGroup; /** Set this if rebinning w/ fixed bin size */
    bool    m_useVariableBins;
    int     m_newNBins;  /** Number of bins to set if rebinning with variable bin size */
    double* m_newBins;   /** Array with variable bin size    */

    bool m_debug;
    bool m_verbose;

    int m_nPtBins_Linear;   /** including underflow and overflow */
    int m_nPtBins_Squared;  /** including underflow and overflow */

    std::vector<std::string> m_obs_selection;

    /**
      The TMinuit object
    */
    TMinuit* m_myFitter;

    /**
      The number of parameters of the fit
    */
    int m_NPAR;

    /**
      Container for the input histograms
    */
    std::vector<TH2D*> m_histograms;

    /**
      Observables
    */
    std::vector<double> m_TelTel;
    std::vector<double> m_TelLel;
    std::vector<double> m_LelTel;
    std::vector<double> m_LelLel;
    std::vector<double> m_TmuTmu;
    std::vector<double> m_TmuLmu;
    std::vector<double> m_LmuTmu;
    std::vector<double> m_LmuLmu;
    std::vector<double> m_TmuTel;
    std::vector<double> m_TmuLel;
    std::vector<double> m_LmuTel;
    std::vector<double> m_LmuLel;
    std::vector<double> m_TelTmu;
    std::vector<double> m_TelLmu;
    std::vector<double> m_LelTmu;
    std::vector<double> m_LelLmu;

    /**
      Initial values for parameters
    */
    std::vector<double> m_rel_init;
    double		m_rel_init_avg;
    std::vector<double> m_fel_init;
    double		m_fel_init_avg;
    std::vector<double> m_rmu_init;
    double		m_rmu_init_avg;
    std::vector<double> m_fmu_init;
    double		m_fmu_init_avg;

    std::vector<double> m_RelRel_init;
    std::vector<double> m_RelFel_init;
    std::vector<double> m_FelRel_init;
    //std::vector<double> m_FelFel_init;
    std::vector<double> m_RmuRmu_init;
    std::vector<double> m_RmuFmu_init;
    std::vector<double> m_FmuRmu_init;
    //std::vector<double> m_FmuFmu_init;
    std::vector<double> m_RmuRel_init;
    std::vector<double> m_RmuFel_init;
    std::vector<double> m_FmuRel_init;
    //std::vector<double> m_FmuFel_init;
    std::vector<double> m_RelRmu_init;
    std::vector<double> m_RelFmu_init;
    std::vector<double> m_FelRmu_init;
    //std::vector<double> m_FelFmu_init;

    /**
      Final parameter values
    */
    std::vector<double> m_rel_vals;
    std::vector<double> m_fel_vals;
    std::vector<double> m_rmu_vals;
    std::vector<double> m_fmu_vals;

    std::vector<double> m_RelRel_vals;
    std::vector<double> m_RelFel_vals;
    std::vector<double> m_FelRel_vals;
    //std::vector<double> m_FelFel_vals;
    std::vector<double> m_RmuRmu_vals;
    std::vector<double> m_RmuFmu_vals;
    std::vector<double> m_FmuRmu_vals;
    //std::vector<double> m_FmuFmu_vals;
    std::vector<double> m_RmuRel_vals;
    std::vector<double> m_RmuFel_vals;
    std::vector<double> m_FmuRel_vals;
    //std::vector<double> m_FmuFel_vals;
    std::vector<double> m_RelRmu_vals;
    std::vector<double> m_RelFmu_vals;
    std::vector<double> m_FelRmu_vals;
    //std::vector<double> m_FelFmu_vals;

    /**
      Final parameter asymmetric errors

      Values in the tuple correspond to:

      [0] --> eplus ( MINOS error UP )
      [1] --> eminus ( MINOS error DN )
      [2] --> eparab ( 'parabolic' error (from error matrix) )

    */
    std::vector<std::tuple<double,double,double> > m_rel_errs;
    std::vector<std::tuple<double,double,double> > m_fel_errs;
    std::vector<std::tuple<double,double,double> > m_rmu_errs;
    std::vector<std::tuple<double,double,double> > m_fmu_errs;

    std::vector<std::tuple<double,double,double> > m_RelRel_errs;
    std::vector<std::tuple<double,double,double> > m_RelFel_errs;
    std::vector<std::tuple<double,double,double> > m_FelRel_errs;
    //std::vector<std::tuple<double,double,double> > m_FelFel_errs;
    std::vector<std::tuple<double,double,double> > m_RmuRmu_errs;
    std::vector<std::tuple<double,double,double> > m_RmuFmu_errs;
    std::vector<std::tuple<double,double,double> > m_FmuRmu_errs;
    //std::vector<std::tuple<double,double,double> > m_FmuFmu_errs;
    std::vector<std::tuple<double,double,double> > m_RmuRel_errs;
    std::vector<std::tuple<double,double,double> > m_RmuFel_errs;
    std::vector<std::tuple<double,double,double> > m_FmuRel_errs;
    //std::vector<std::tuple<double,double,double> > m_FmuFel_errs;
    std::vector<std::tuple<double,double,double> > m_RelRmu_errs;
    std::vector<std::tuple<double,double,double> > m_RelFmu_errs;
    std::vector<std::tuple<double,double,double> > m_FelRmu_errs;
    //std::vector<std::tuple<double,double,double> > m_FelFmu_errs;

    std::string m_input_path_TP;
    std::string m_input_path_yields;

    /**
      Function to get number of bins below (and including) diagonal in N X N 2D hist
    */
    inline int areaGrid( const int& n );

    /**
      Get tag and probe efficiencies from input file
    */
    void readTagAndProbeEff();

    /**
      Get input histograms for TT, TL, LT, LL from ROOT file
      Read the TT, TL, LT, LL events bin-by-bin from input histograms
    */
    void getHists();

    /**
      Find initial guesses for parameters. Use inputs from tag-and-probe measurement
    */
    void getEducatedGuess();

    /**
      Reset global flags
    */
    void resetGlobFlags();

    /**
      Update the content of error containers w/ info from MINOS
    */
    void getParametersAndErrors();

    /**
      Save efficiencies and their errors in a ROOT/text file
    */
    void  saveEfficiencies();

};

double LHFitter::s_step_eff    = 1e-3;
double LHFitter::s_up_eff      = 1.0;
double LHFitter::s_dn_eff      = 0.0;
double LHFitter::s_step_yields = 1e-3;
double LHFitter::s_up_yields   = 1e6;
double LHFitter::s_dn_yields   = 0.0;

// ----------------------------------------------------------------------------------------------------------------------

LHFitter :: LHFitter( kFlavour FLAVOUR, kEfficiency EFFICIENCY ) :
  m_debug(false),
  m_verbose(false),
  m_doSubtraction(false),
  m_doRebinning(false),
  m_nBinGroup(1),
  m_useVariableBins(false),
  m_newBins(nullptr),
  m_myFitter(nullptr),
  m_obs_selection({"TT","TL","LT","LL"}),
  m_r_init_avg(0.0),
  m_f_init_avg(0.0)
{

  m_flavour = FLAVOUR;
  m_efficiency = EFFICIENCY;

  if ( m_efficiency == kEfficiency::REAL ) { m_efficiency_str = "REAL"; }
  if ( m_efficiency == kEfficiency::FAKE ) { m_efficiency_str = "FAKE"; }
  if ( m_flavour == kFlavour::ELEC ) { m_flavour_str = "ELECTRON"; }
  if ( m_flavour == kFlavour::MUON ) { m_flavour_str = "MUON"; }
  if ( m_flavour == kFlavour::INCLUSIVE ) { m_flavour_str = "INCLUSIVE"; }

  Info("LHFitter()","Creating class instance to fit %s efficiency for %s... \n", m_efficiency_str.c_str(), m_flavour_str.c_str() );

  // Every time an instance is created, the global variables must be reset, no matter what
  //
  this->resetGlobFlags();
}

// ----------------------------------------------------------------------------------------------------------------------

LHFitter::~LHFitter() {
  if ( m_newBins != nullptr )  delete[] m_newBins;
}

// ----------------------------------------------------------------------------------------------------------------------

void LHFitter :: initialise() {

  Info("initialise()","Setting up fit...");

  // Get input histograms and store them
  //
  this->getHists();

  // Reserve memory for (initial) parameter containers
  //
  m_rel_init.reserve(m_nPtBins_Linear);
  m_fel_init.reserve(m_nPtBins_Linear);
  m_rmu_init.reserve(m_nPtBins_Linear);
  m_fmu_init.reserve(m_nPtBins_Linear);

  m_RelRel_init.reserve(m_nPtBins_Squared);
  m_RelFel_init.reserve(m_nPtBins_Squared);
  m_FelRel_init.reserve(m_nPtBins_Squared);
  //m_FelFel_init.reserve(m_nPtBins_Squared);
  m_RmuRmu_init.reserve(m_nPtBins_Squared);
  m_RmuFmu_init.reserve(m_nPtBins_Squared);
  m_FmuRmu_init.reserve(m_nPtBins_Squared);
  //m_FmuFmu_init.reserve(m_nPtBins_Squared);
  m_RmuRel_init.reserve(m_nPtBins_Squared);
  m_RmuFel_init.reserve(m_nPtBins_Squared);
  m_FmuRel_init.reserve(m_nPtBins_Squared);
  //m_FmuFel_init.reserve(m_nPtBins_Squared);
  m_RelRmu_init.reserve(m_nPtBins_Squared);
  m_RelFmu_init.reserve(m_nPtBins_Squared);
  m_FelRmu_init.reserve(m_nPtBins_Squared);
  //m_FelFmu_init.reserve(m_nPtBins_Squared);

  if ( m_verbose ) {
     printContainer( m_TelTel, "Printing content of TelTel:" );
     printContainer( m_TelLel, "Printing content of TelLel:" );
     printContainer( m_LelTel, "Printing content of LelTel:" );
     printContainer( m_LelLel, "Printing content of LelLel:" );

     printContainer( m_TmuTmu, "Printing content of TmuTmu:" );
     printContainer( m_TmuLmu, "Printing content of TmuLmu:" );
     printContainer( m_LmuTmu, "Printing content of LmuTmu:" );
     printContainer( m_LmuLmu, "Printing content of LmuLmu:" );

     printContainer( m_TmuTel, "Printing content of TmuTel:" );
     printContainer( m_TmuLel, "Printing content of TmuLel:" );
     printContainer( m_LmuTel, "Printing content of LmuTel:" );
     printContainer( m_LmuLel, "Printing content of LmuLel:" );

     printContainer( m_TelTmu, "Printing content of TelTmu:" );
     printContainer( m_TelLmu, "Printing content of TelLmu:" );
     printContainer( m_LelTmu, "Printing content of LelTmu:" );
     printContainer( m_LelLmu, "Printing content of LelLmu:" );
  }

  std::string eff_type("");
  std::string flavour("");

  // Set the number of parameteres of the fit
  //
  int NFLAV(0);
  if ( m_flavour == kFlavour::ELEC || m_flavour == kFlavour::MUON ) {
    NFLAV = 1;
  }
  if ( m_flavour == kFlavour::INCLUSIVE ) {
    NFLAV = 4;
  }

  int NCOMP(0);
  if ( m_efficiency == kEfficiency::REAL ) {
    NCOMP = 1; // RR only
  }
  if ( m_efficiency == kEfficiency::FAKE ) {
   //NCOMP = 3; // RF, FR, FF
    NCOMP = 2; // RF, FR
  }

  std::cout << "" << std::endl;
  std::cout << " Number of 1D pT bins (including O/Flow) = "<<  m_nPtBins_Linear << std::endl;
  std::cout << " Number of effective 2D pT bins (including O/Flow) = "<<  m_nPtBins_Squared << std::endl;
  std::cout << " ----------------------------"<<  std::endl;
  std::cout << " Number of flavour bins = "<<  NFLAV << std::endl;
  std::cout << " Number of RR, RF, FR, FF bins = "<<  NCOMP << std::endl;
  std::cout << "" << std::endl;

  // Total number of parameters to be estimated in the fit
  //
  // 1st factor in sum: YIELDS
  // 2nd factor in sum: EFFICIENCIES
  //
  const int NPAR_YIELDS = m_nPtBins_Squared * NFLAV * NCOMP;
  const int NPAR_EFF	= m_nPtBins_Linear;

  m_NPAR = NPAR_YIELDS + NPAR_EFF;

  const int m_NOBS = m_obs_selection.size() * m_nPtBins_Squared;

  Info("initialise()","Number of observables in fit ===> %i", m_NOBS);
  Info("initialise()","Number of free parameters in fit ===> %i (efficiencies) + %i (yields) = %i\n", NPAR_EFF, NPAR_YIELDS, m_NPAR);

  int ierflg(0);

  // Create the TMinuit object
  //
  m_myFitter = new TMinuit(m_NPAR);

  // Set the fitting function
  //
  m_myFitter->SetFCN(myLikelihood);

  // Get an educated guess for the initial parameters, from the tag-and-probe measurement:
  //
  // r(i), f(i)  ( in 1D bins of pT )
  //
  // RR(j,k), RF(j,k), FR(j,k), FF(j,k) ( in 2D bins of lead-sublead pT )
  //
  this->getEducatedGuess();

  if ( m_debug ) {
     printContainer( m_rel_init, "Printing content of rel_init:" );
     printContainer( m_fel_init, "Printing content of fel_init:" );
     printContainer( m_rmu_init, "Printing content of rmu_init:" );
     printContainer( m_fmu_init, "Printing content of fmu_init:" );
     if ( m_efficiency == kEfficiency::REAL ) {
	 printContainer( m_RelRel_init,"Printing content of RelRel_init:" );
	 printContainer( m_RmuRmu_init,"Printing content of RmuRmu_init:" );
	 printContainer( m_RmuRel_init,"Printing content of RmuRel_init:" );
	 printContainer( m_RelRmu_init,"Printing content of RelRmu_init:" );
     }
     if ( m_efficiency == kEfficiency::FAKE ) {
	 printContainer( m_RelFel_init,"Printing content of RelFel_init:" );
	 printContainer( m_FelRel_init,"Printing content of FelRel_init:" );
	 //printContainer( m_FelFel_init,"Printing content of FelFel_init:" );
	 printContainer( m_RmuFmu_init,"Printing content of RmuFmu_init:" );
	 printContainer( m_FmuRmu_init,"Printing content of FmuRmu_init:" );
	 //printContainer( m_FmuFmu_init,"Printing content of FmuFmu_init:" );
	 printContainer( m_RmuFel_init,"Printing content of RmuFel_init:" );
	 printContainer( m_FmuRel_init,"Printing content of FmuRel_init:" );
	 //printContainer( m_FmuFel_init,"Printing content of FmuFel_init:" );
	 printContainer( m_RelFmu_init,"Printing content of RelFmu_init:" );
	 printContainer( m_FelRmu_init,"Printing content of FelRmu_init:" );
	 //printContainer( m_FelFmu_init,"Printing content of FelFmu_init:" );
     }
     printContainer( g_TelTel_resized, "Printing content of TelTel (resized):" );
     printContainer( g_TelLel_resized, "Printing content of TelLel (resized):" );
     printContainer( g_LelTel_resized, "Printing content of LelTel (resized):" );
     printContainer( g_LelLel_resized, "Printing content of LelLel (resized):" );

     printContainer( g_TmuTmu_resized, "Printing content of TmuTmu (resized):" );
     printContainer( g_TmuLmu_resized, "Printing content of TmuLmu (resized):" );
     printContainer( g_LmuTmu_resized, "Printing content of LmuTmu (resized):" );
     printContainer( g_LmuLmu_resized, "Printing content of LmuLmu (resized):" );

     printContainer( g_TmuTel_resized, "Printing content of TmuTel (resized):" );
     printContainer( g_TmuLel_resized, "Printing content of TmuLel (resized):" );
     printContainer( g_LmuTel_resized, "Printing content of LmuTel (resized):" );
     printContainer( g_LmuLel_resized, "Printing content of LmuLel (resized):" );

     printContainer( g_TelTmu_resized, "Printing content of TelTmu (resized):" );
     printContainer( g_TelLmu_resized, "Printing content of TelLmu (resized):" );
     printContainer( g_LelTmu_resized, "Printing content of LelTmu (resized):" );
     printContainer( g_LelLmu_resized, "Printing content of LelLmu (resized):" );

  }

  // Set the parameters of the fit into the toatl par[] array of the TMinuit object
  // The order will be:
  // -) r  ( x nPtBins_Linear )
  // -) f  ( x nPtBins_Linear )
  // -) RR ( x nPtBins_Squared )
  // -) RF ( x nPtBins_Squared )
  // -) FR ( x nPtBins_Squared )
  // -) FF ( x nPtBins_Squared )

  // Set parameters for r,f efficiencies. This is just a 1D loop over pT bins
  //
  std::string param_name("");
  int offset(0); // needed for setting parameter offsets (TMinuit can accept only one huge array of parameters...)
  int param_idx(0);

  // --------------------
  // Set parameters for r
  // --------------------

  if ( m_efficiency == kEfficiency::REAL ) {

    g_reff = true;

    if ( m_flavour == kFlavour::ELEC || m_flavour == kFlavour::INCLUSIVE ) {

	for ( auto ibin(0); ibin < m_nPtBins_Linear; ++ibin ) {
	    param_name = "real efficiency - el - bin [" + std::to_string(ibin) + "]";
	    param_idx  = offset + ibin;
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_rel_init.at(ibin), s_step_eff, s_dn_eff, s_up_eff, ierflg );
	    g_rel_idxs.push_back( param_idx );
	}

	// A trick: save the index of the bin for the real efficiency for every (lead, sublead) lepton pair
	// It will contain the same indexes of r_idxs, but each one repeated nPtBins_Linear times
	//
	for ( int ibiny(0); ibiny < m_nPtBins_Linear; ++ibiny ) {
	    for ( int ibinx(0); ibinx < m_nPtBins_Linear; ++ibinx ) {
		if ( ibiny > ibinx ) { continue; }
		g_r1el_idxs.push_back( ibinx );
		g_r2el_idxs.push_back( ibiny );
	    }
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Linear;

    }
    if ( m_flavour == kFlavour::MUON || m_flavour == kFlavour::INCLUSIVE ) {

	for ( auto ibin(0); ibin < m_nPtBins_Linear; ++ibin ) {
	    param_name = "real efficiency - mu - bin [" + std::to_string(ibin) + "]";
	    param_idx  = offset + ibin;
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_rmu_init.at(ibin), s_step_eff, s_dn_eff, s_up_eff, ierflg );
	    g_rmu_idxs.push_back( param_idx );
	}

	// A trick: save the index of the bin for the real efficiency for every (lead, sublead) lepton pair
	// It will contain the same indexes of r_idxs, but each one repeated nPtBins_Linear times
	//
	for ( int ibiny(0); ibiny < m_nPtBins_Linear; ++ibiny ) {
	    for ( int ibinx(0); ibinx < m_nPtBins_Linear; ++ibinx ) {
		if ( ibiny > ibinx ) { continue; }
		g_r1mu_idxs.push_back( ibinx );
		g_r2mu_idxs.push_back( ibiny );
	    }
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Linear;

    }

  }

  // --------------------
  // Set parameters for f
  // --------------------

  if ( m_efficiency == kEfficiency::FAKE ) {

    g_feff = true;

    if ( m_flavour == kFlavour::ELEC || m_flavour == kFlavour::INCLUSIVE ) {

	for ( auto ibin(0); ibin < m_nPtBins_Linear; ++ibin ) {
	    param_name = "fake efficiency - el - bin [" + std::to_string(ibin) + "]";
	    param_idx  = offset + ibin;
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_fel_init.at(ibin), s_step_eff, s_dn_eff, s_up_eff, ierflg );
	    g_fel_idxs.push_back( param_idx );
	}

	// A trick: save the index of the bin for the real efficiency for every (lead, sublead) lepton pair
	// It will contain the same indexes of f_idxs, but each one repeated nPtBins_Linear times
	//
	for ( int ibiny(0); ibiny < m_nPtBins_Linear; ++ibiny ) {
	    for ( int ibinx(0); ibinx < m_nPtBins_Linear; ++ibinx ) {
		if ( ibiny > ibinx ) { continue; }
		g_f1el_idxs.push_back( ibinx );
		g_f2el_idxs.push_back( ibiny );
	    }
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Linear;
    }
    if ( m_flavour == kFlavour::MUON || m_flavour == kFlavour::INCLUSIVE ) {

	for ( auto ibin(0); ibin < m_nPtBins_Linear; ++ibin ) {
	    param_name = "fake efficiency - mu - bin [" + std::to_string(ibin) + "]";
	    param_idx  = offset + ibin;
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_fmu_init.at(ibin), s_step_eff, s_dn_eff, s_up_eff, ierflg );
	    g_fmu_idxs.push_back( param_idx );
	}

	// A trick: save the index of the bin for the real efficiency for every (lead, sublead) lepton pair
	// It will contain the same indexes of f_idxs, but each one repeated nPtBins_Linear times
	//
	for ( int ibiny(0); ibiny < m_nPtBins_Linear; ++ibiny ) {
	    for ( int ibinx(0); ibinx < m_nPtBins_Linear; ++ibinx ) {
		if ( ibiny > ibinx ) { continue; }
		g_f1mu_idxs.push_back( ibinx );
		g_f2mu_idxs.push_back( ibiny );
	    }
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Linear;
    }

  }

  // ---------------------
  // Set parameters for RR
  // ---------------------

  if ( m_efficiency == kEfficiency::REAL ) {

    g_RR = true;

    if ( m_flavour == kFlavour::ELEC || m_flavour == kFlavour::INCLUSIVE ) {
	for ( auto ibin(0); ibin < m_nPtBins_Squared; ++ibin ) {
	    param_name = "RelRel - bin [" + std::to_string(ibin) + "]";
	    param_idx = offset + ibin; // can use any of the input histograms: take the first by default
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_RelRel_init.at(ibin), s_step_yields, s_dn_yields, s_up_yields, ierflg );
	    g_RelRel_idxs.push_back( param_idx );
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Squared;
    }
    if ( m_flavour == kFlavour::MUON || m_flavour == kFlavour::INCLUSIVE ) {
	for ( auto ibin(0); ibin < m_nPtBins_Squared; ++ibin ) {
	    param_name = "RmuRmu - bin [" + std::to_string(ibin) + "]";
	    param_idx = offset + ibin; // can use any of the input histograms: take the first by default
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_RmuRmu_init.at(ibin), s_step_yields, s_dn_yields, s_up_yields, ierflg );
	    g_RmuRmu_idxs.push_back( param_idx );
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Squared;
    }
    if ( m_flavour == kFlavour::INCLUSIVE ) {
 	for ( auto ibin(0); ibin < m_nPtBins_Squared; ++ibin ) {
	    param_name = "RmuRel - bin [" + std::to_string(ibin) + "]";
	    param_idx = offset + ibin; // can use any of the input histograms: take the first by default
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_RmuRel_init.at(ibin), s_step_yields, s_dn_yields, s_up_yields, ierflg );
	    g_RmuRel_idxs.push_back( param_idx );
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Squared;

 	for ( auto ibin(0); ibin < m_nPtBins_Squared; ++ibin ) {
	    param_name = "RelRmu - bin [" + std::to_string(ibin) + "]";
	    param_idx = offset + ibin; // can use any of the input histograms: take the first by default
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_RelRmu_init.at(ibin), s_step_yields, s_dn_yields, s_up_yields, ierflg );
	    g_RelRmu_idxs.push_back( param_idx );
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Squared;
    }

  }
  // ---------------------
  // Set parameters for RF
  // ---------------------

  if ( m_efficiency == kEfficiency::FAKE ) {

    g_RF = true;

    if ( m_flavour == kFlavour::ELEC || m_flavour == kFlavour::INCLUSIVE ) {
	for ( auto ibin(0); ibin < m_nPtBins_Squared; ++ibin ) {
	    param_name = "RelFel - bin [" + std::to_string(ibin) + "]";
	    param_idx = offset + ibin; // can use any of the input histograms: take the first by default
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_RelFel_init.at(ibin), s_step_yields, s_dn_yields, s_up_yields, ierflg );
	    g_RelFel_idxs.push_back( param_idx );
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Squared;
    }
    if ( m_flavour == kFlavour::MUON || m_flavour == kFlavour::INCLUSIVE ) {
	for ( auto ibin(0); ibin < m_nPtBins_Squared; ++ibin ) {
	    param_name = "RmuFmu - bin [" + std::to_string(ibin) + "]";
	    param_idx = offset + ibin; // can use any of the input histograms: take the first by default
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_RmuFmu_init.at(ibin), s_step_yields, s_dn_yields, s_up_yields, ierflg );
	    g_RmuFmu_idxs.push_back( param_idx );
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Squared;
    }
    if ( m_flavour == kFlavour::INCLUSIVE ) {
 	for ( auto ibin(0); ibin < m_nPtBins_Squared; ++ibin ) {
	    param_name = "RmuFel - bin [" + std::to_string(ibin) + "]";
	    param_idx = offset + ibin; // can use any of the input histograms: take the first by default
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_RmuFel_init.at(ibin), s_step_yields, s_dn_yields, s_up_yields, ierflg );
	    g_RmuFel_idxs.push_back( param_idx );
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Squared;

 	for ( auto ibin(0); ibin < m_nPtBins_Squared; ++ibin ) {
	    param_name = "RelFmu - bin [" + std::to_string(ibin) + "]";
	    param_idx = offset + ibin; // can use any of the input histograms: take the first by default
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_RelFmu_init.at(ibin), s_step_yields, s_dn_yields, s_up_yields, ierflg );
	    g_RelFmu_idxs.push_back( param_idx );
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Squared;
    }
  }
  // ---------------------
  // Set parameters for FR
  // ---------------------

  if ( m_efficiency == kEfficiency::FAKE ) {

    g_FR = true;

    if ( m_flavour == kFlavour::ELEC || m_flavour == kFlavour::INCLUSIVE ) {
	for ( auto ibin(0); ibin < m_nPtBins_Squared; ++ibin ) {
	    param_name = "FelRel - bin [" + std::to_string(ibin) + "]";
	    param_idx = offset + ibin; // can use any of the input histograms: take the first by default
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_FelRel_init.at(ibin), s_step_yields, s_dn_yields, s_up_yields, ierflg );
	    g_FelRel_idxs.push_back( param_idx );
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Squared;
    }
    if ( m_flavour == kFlavour::MUON || m_flavour == kFlavour::INCLUSIVE ) {
	for ( auto ibin(0); ibin < m_nPtBins_Squared; ++ibin ) {
	    param_name = "FmuRmu - bin [" + std::to_string(ibin) + "]";
	    param_idx = offset + ibin; // can use any of the input histograms: take the first by default
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_FmuRmu_init.at(ibin), s_step_yields, s_dn_yields, s_up_yields, ierflg );
	    g_FmuRmu_idxs.push_back( param_idx );
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Squared;
    }
    if ( m_flavour == kFlavour::INCLUSIVE ) {
 	for ( auto ibin(0); ibin < m_nPtBins_Squared; ++ibin ) {
	    param_name = "FmuRel - bin [" + std::to_string(ibin) + "]";
	    param_idx = offset + ibin; // can use any of the input histograms: take the first by default
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_FmuRel_init.at(ibin), s_step_yields, s_dn_yields, s_up_yields, ierflg );
	    g_FmuRel_idxs.push_back( param_idx );
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Squared;

 	for ( auto ibin(0); ibin < m_nPtBins_Squared; ++ibin ) {
	    param_name = "FelRmu - bin [" + std::to_string(ibin) + "]";
	    param_idx = offset + ibin; // can use any of the input histograms: take the first by default
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_FelRmu_init.at(ibin), s_step_yields, s_dn_yields, s_up_yields, ierflg );
	    g_FelRmu_idxs.push_back( param_idx );
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Squared;
    }
  }

  // ---------------------
  // Set parameters for FF
  // ---------------------

  /*
  if ( m_efficiency == kEfficiency::FAKE ) {

    g_FF = true;

    if ( m_flavour == kFlavour::ELEC || m_flavour == kFlavour::INCLUSIVE ) {
	for ( auto ibin(0); ibin < m_nPtBins_Squared; ++ibin ) {
	    param_name = "FelFel - bin [" + std::to_string(ibin) + "]";
	    param_idx = offset + ibin; // can use any of the input histograms: take the first by default
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_FelFel_init.at(ibin), s_step_yields, s_dn_yields, s_up_yields, ierflg );
	    g_FelFel_idxs.push_back( param_idx );
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Squared;
    }
    if ( m_flavour == kFlavour::MUON || m_flavour == kFlavour::INCLUSIVE ) {
	for ( auto ibin(0); ibin < m_nPtBins_Squared; ++ibin ) {
	    param_name = "FmuFmu - bin [" + std::to_string(ibin) + "]";
	    param_idx = offset + ibin; // can use any of the input histograms: take the first by default
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_FmuFmu_init.at(ibin), s_step_yields, s_dn_yields, s_up_yields, ierflg );
	    g_FmuFmu_idxs.push_back( param_idx );
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Squared;
    }
    if ( m_flavour == kFlavour::INCLUSIVE ) {
 	for ( auto ibin(0); ibin < m_nPtBins_Squared; ++ibin ) {
	    param_name = "FmuFel - bin [" + std::to_string(ibin) + "]";
	    param_idx = offset + ibin; // can use any of the input histograms: take the first by default
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_FmuFel_init.at(ibin), s_step_yields, s_dn_yields, s_up_yields, ierflg );
	    g_FmuFel_idxs.push_back( param_idx );
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Squared;

 	for ( auto ibin(0); ibin < m_nPtBins_Squared; ++ibin ) {
	    param_name = "FelFmu - bin [" + std::to_string(ibin) + "]";
	    param_idx = offset + ibin; // can use any of the input histograms: take the first by default
	    m_myFitter->mnparm( param_idx, param_name.c_str(), m_FelFmu_init.at(ibin), s_step_yields, s_dn_yields, s_up_yields, ierflg );
	    g_FelFmu_idxs.push_back( param_idx );
	}
	// Set the offset for total parameter index
	//
	offset += m_nPtBins_Squared;
    }
  }
  */

  // Set default values for final parameter/error vectors
  //
  int idx1(0);
  while ( idx1 < m_nPtBins_Linear ) {
    m_rel_vals.push_back(0.0);
    m_fel_vals.push_back(0.0);
    m_rmu_vals.push_back(0.0);
    m_fmu_vals.push_back(0.0);
    m_rel_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    m_fel_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    m_rmu_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    m_fmu_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    ++idx1;
  }
  int idx2(0);
  while ( idx2 < m_nPtBins_Squared ) {
    m_RelRel_vals.push_back(0.0);
    m_RelFel_vals.push_back(0.0);
    m_FelRel_vals.push_back(0.0);
    //m_FelFel_vals.push_back(0.0);
    m_RmuRmu_vals.push_back(0.0);
    m_RmuFmu_vals.push_back(0.0);
    m_FmuRmu_vals.push_back(0.0);
    //m_FmuFmu_vals.push_back(0.0);
    m_RmuRel_vals.push_back(0.0);
    m_RmuFel_vals.push_back(0.0);
    m_FmuRel_vals.push_back(0.0);
    //m_FmuFel_vals.push_back(0.0);
    m_RelRmu_vals.push_back(0.0);
    m_RelFmu_vals.push_back(0.0);
    m_FelRmu_vals.push_back(0.0);
    //m_FelFmu_vals.push_back(0.0);
    m_RelRel_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    m_RelFel_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    m_FelRel_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    //m_FelFel_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    m_RmuRmu_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    m_RmuFmu_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    m_FmuRmu_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    //m_FmuFmu_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    m_RmuRel_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    m_RmuFel_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    m_FmuRel_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    //m_FmuFel_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    m_RelRmu_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    m_RelFmu_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    m_FelRmu_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    //m_FelFmu_errs.push_back(std::make_tuple( 0.0, 0.0, 0.0 ));
    ++idx2;
  }

  if ( m_verbose ) {
      if ( m_efficiency == kEfficiency::REAL ) {
	  printContainer( g_rel_idxs, "Printing content of rel_idxs:" );
	  printContainer( g_r1el_idxs, "Printing content of r1el_idxs:" );
	  printContainer( g_r2el_idxs, "Printing content of r2el_idxs:" );
	  printContainer( g_rmu_idxs, "Printing content of rmu_idxs:" );
	  printContainer( g_r1mu_idxs, "Printing content of r1mu_idxs:" );
	  printContainer( g_r2mu_idxs, "Printing content of r2mu_idxs:" );
      }
      if ( m_efficiency == kEfficiency::FAKE ) {
	  printContainer( g_fel_idxs, "Printing content of fel_idxs:" );
	  printContainer( g_f1el_idxs, "Printing content of f1el_idxs:" );
	  printContainer( g_f2el_idxs, "Printing content of f2el_idxs:" );
	  printContainer( g_fmu_idxs, "Printing content of fmu_idxs:" );
	  printContainer( g_f1mu_idxs, "Printing content of f1mu_idxs:" );
	  printContainer( g_f2mu_idxs, "Printing content of f2mu_idxs:" );
      }
      if ( m_efficiency == kEfficiency::REAL ) {
	  printContainer( g_RelRel_idxs, "Printing content of RelRel_idxs:" );
	  printContainer( g_RmuRmu_idxs, "Printing content of RmuRmu_idxs:" );
	  printContainer( g_RmuRel_idxs, "Printing content of RmuRel_idxs:" );
	  printContainer( g_RelRmu_idxs, "Printing content of RelRmu_idxs:" );
      }
      if ( m_efficiency == kEfficiency::FAKE ) {
	  printContainer( g_RelFel_idxs, "Printing content of RelFel_idxs:" );
	  printContainer( g_FelRel_idxs, "Printing content of FelRel_idxs:" );
	  //printContainer( g_FelFel_idxs, "Printing content of FelFel_idxs:" );
	  printContainer( g_RmuFmu_idxs, "Printing content of RmuFmu_idxs:" );
	  printContainer( g_FmuRmu_idxs, "Printing content of FmuRmu_idxs:" );
	  //printContainer( g_FmuFmu_idxs, "Printing content of FmuFmu_idxs:" );
	  printContainer( g_RmuFel_idxs, "Printing content of RmuFel_idxs:" );
	  printContainer( g_FmuRel_idxs, "Printing content of FmuRel_idxs:" );
	  //printContainer( g_FmuFel_idxs, "Printing content of FmuFel_idxs:" );
	  printContainer( g_RelFmu_idxs, "Printing content of RelFmu_idxs:" );
	  printContainer( g_FelRmu_idxs, "Printing content of FelRmu_idxs:" );
	  //printContainer( g_FelFmu_idxs, "Printing content of FelFmu_idxs:" );
      }
  }

  Info("initialise()","Initialisation done!");

}
// ----------------------------------------------------------------------------------------------------------------------

void LHFitter :: fit() {

  std::cout << "" << std::endl;
  Info("fit()","Performing the fit...\n" );

  double arglist[m_NPAR];
  int ierflg(0);

  arglist[0] = 1000; // maximum number of iterations
  m_myFitter->mnexcm("MIGRAD",arglist,2/*0*/,ierflg);

  std::cout << "\n\n" << std::endl;

  if ( !m_myFitter->fCstatu.Contains("CONVERGED") ) {
    Error("fit()","No convergence at fitting! Minuit return string: %s", m_myFitter->fCstatu.Data() );
    //exit(-1);
  }

  arglist[0] = 0.0;
  arglist[1] = 1.0;
  m_myFitter->mnexcm("MINOS",arglist,1,ierflg); // calculate MINOS errors for all the parameters

  if ( m_verbose ) {
    if ( m_efficiency == kEfficiency::REAL ) {
      printContainer( m_rel_vals, "Printing content of rel_vals (DEFAULT):" );
      printErrorContainer( m_rel_errs, "Printing content of rel_errs (DEFAULT):" );
      printContainer( m_rmu_vals, "Printing content of rmu_vals (DEFAULT):" );
      printErrorContainer( m_rmu_errs, "Printing content of rmu_errs (DEFAULT):" );
      printContainer( m_RelRel_vals, "Printing content of RelRel_vals (DEFAULT):" );
      printErrorContainer( m_RelRel_errs, "Printing content of RelRel_errs (DEFAULT):" );
      printContainer( m_RmuRmu_vals, "Printing content of RmuRmu_vals (DEFAULT):" );
      printErrorContainer( m_RmuRmu_errs, "Printing content of RmuRmu_errs (DEFAULT):" );
      printContainer( m_RmuRel_vals, "Printing content of RmuRel_vals (DEFAULT):" );
      printErrorContainer( m_RmuRel_errs, "Printing content of RmuRel_errs (DEFAULT):" );
      printContainer( m_RelRmu_vals, "Printing content of RelRmu_vals (DEFAULT):" );
      printErrorContainer( m_RelRmu_errs, "Printing content of RelRmu_errs (DEFAULT):" );
    }
    if ( m_efficiency == kEfficiency::FAKE ) {
      printContainer( m_fel_vals, "Printing content of fel_vals (DEFAULT):" );
      printErrorContainer( m_fel_errs, "Printing content of fel_errs (DEFAULT):" );
      printContainer( m_fmu_vals, "Printing content of fmu_vals (DEFAULT):" );
      printErrorContainer( m_fmu_errs, "Printing content of fmu_errs (DEFAULT):" );

      printContainer( m_RelFel_vals, "Printing content of RelFel_vals (DEFAULT):" );
      printErrorContainer( m_RelFel_errs, "Printing content of RelFel_errs (DEFAULT):" );
      printContainer( m_FelRel_vals, "Printing content of FelRel_vals (DEFAULT):" );
      printErrorContainer( m_FelRel_errs, "Printing content of FelRel_errs (DEFAULT):" );

      printContainer( m_RmuFmu_vals, "Printing content of RmuFmu_vals (DEFAULT):" );
      printErrorContainer( m_RmuFmu_errs, "Printing content of RmuFmu_errs (DEFAULT):" );
      printContainer( m_FmuRmu_vals, "Printing content of FmuRmu_vals (DEFAULT):" );
      printErrorContainer( m_FmuRmu_errs, "Printing content of FmuRmu_errs (DEFAULT):" );

      printContainer( m_RmuFel_vals, "Printing content of RmuFel_vals (DEFAULT):" );
      printErrorContainer( m_RmuFel_errs, "Printing content of RmuFel_errs (DEFAULT):" );
      printContainer( m_FmuRel_vals, "Printing content of FmuRel_vals (DEFAULT):" );
      printErrorContainer( m_FmuRel_errs, "Printing content of FmuRel_errs (DEFAULT):" );

      printContainer( m_RelFmu_vals, "Printing content of RelFmu_vals (DEFAULT):" );
      printErrorContainer( m_RelFmu_errs, "Printing content of RelFmu_errs (DEFAULT):" );
      printContainer( m_FelRmu_vals, "Printing content of FelRmu_vals (DEFAULT):" );
      printErrorContainer( m_FelRmu_errs, "Printing content of FelRmu_errs (DEFAULT):" );
    }
  }

  // Get final parameters, parabolic error and the asymmetric errors from MINOS
  //
  this->getParametersAndErrors();

  if ( m_debug ) {
    if ( m_efficiency == kEfficiency::REAL ) {
      printContainer( m_r_vals, "Printing content of r_vals (POST-FIT):" );
      printErrorContainer( m_r_errs, "Printing content of r_errs (POST-FIT):" );
      printContainer( m_RR_vals, "Printing content of RR_vals (POST-FIT):" );
      printErrorContainer( m_RR_errs, "Printing content of RR_errs (POST-FIT):" );
      if ( m_flavour == kFlavour::ELEC ) {
        printContainer( g_fitted_r1_el, "Printing content of g_fitted_r1_el (POST-FIT):" );
        printContainer( g_fitted_r2_el, "Printing content of g_fitted_r2_el (POST-FIT):" );
      }
      if ( m_flavour == kFlavour::MUON ) {
        printContainer( g_fitted_r1_mu, "Printing content of g_fitted_r1_mu (POST-FIT):" );
        printContainer( g_fitted_r2_mu, "Printing content of g_fitted_r2_mu (POST-FIT):" );
      }
    }
    if ( m_efficiency == kEfficiency::FAKE ) {
      printContainer( m_f_vals, "Printing content of f_vals (POST-FIT):" );
      printErrorContainer( m_f_errs, "Printing content of f_errs (POST-FIT):" );
      printContainer( m_RF_vals, "Printing content of RF_vals (POST-FIT):" );
      printErrorContainer( m_RF_errs, "Printing content of RF_errs (POST-FIT):" );
      printContainer( m_FR_vals, "Printing content of FR_vals (POST-FIT):" );
      printErrorContainer( m_FR_errs, "Printing content of FR_errs (POST-FIT):" );
    }
  }

  // Save results to output
  //
  this->saveEfficiencies();

  // Print fit statistic
  //
  double best_min;  // the best function value found so far
  double est_vdist; // the estimated vertical distance remaining to minimum
  double err_def;   // the value of UP defining parameter uncertainties
  int nvpar;	    // the number of currently variable parameters
  int nparx;	    // the highest (external) parameter number defined by user
  int icstat;	    // a status integer indicating how good is the covariance matrix:
  		    //  0= not calculated at all
        	    //  1= approximation only, not accurate
        	    //  2= full matrix, but forced positive-definite
        	    //  3= full accurate covariance matrix

  m_myFitter->mnstat(best_min,est_vdist,err_def,nvpar,nparx,icstat);

  std::cout << "" << std::endl;
  Info("fit()","************************************************" );
  std::cout << "" << std::endl;

  switch (icstat) {
   case 0 : Error("fit()","No covariance matrix was calculated! Exiting..." );
  	    exit(-1);
  	    break;
   case 1 : Warning("fit()","An approximated covariance matrix was calculated! Not accurate..." );
  	    break;
   case 2 : Warning("fit()","Full covariance matrix was calculated, but forced to be positive-definite..." );
  	    break;
   case 3 : Info("fit()","Full covariance matrix was calculated :)" );
  	    break;
  }

  Info("fit()","Minimum of likelihood function = %f", best_min );
  Info("fit()","Estimated vert. distance to min. = %f", est_vdist );
  Info("fit()","Value of UP defining parameter unc. = %f", err_def );
  Info("fit()","Number of variable parameters = %i", nvpar );
  Info("fit()","Highest number of parameters defined by user = %i", nparx );
  std::cout << "" << std::endl;
  Info("fit()","************************************************\n" );

}

// ----------------------------------------------------------------------------------------------------------------------

int LHFitter :: areaGrid( const int& n ) {
  int area(0);
  for ( int i = 0; i < n; ++i ) {
    area += n - i;
  }
  return area;
}

// ----------------------------------------------------------------------------------------------------------------------

void LHFitter :: resetGlobFlags(){

  Info("resetGlobFlags()","Resetting all global variables..." );

  g_nPtBins_Squared = 0;

  g_rel_idxs.clear();
  g_fel_idxs.clear();
  g_rmu_idxs.clear();
  g_fmu_idxs.clear();
  g_RelRel_idxs.clear();
  g_FelRel_idxs.clear();
  g_RelFel_idxs.clear();
  //g_FelFel_idxs.clear();
  g_RelRel_idxs.clear();
  g_FelRel_idxs.clear();
  g_RelFel_idxs.clear();
  //g_FelFel_idxs.clear();
  g_r1el_idxs.clear();
  g_r2el_idxs.clear();
  g_f1el_idxs.clear();
  g_f2el_idxs.clear();

  // these should not be reset...
  //g_fitted_r1_el.clear();
  //g_fitted_r2_el.clear();
  //g_fitted_r1_mu.clear();
  //g_fitted_r2_mu.clear();

  g_TT_resized.clear();
  g_TL_resized.clear();
  g_LT_resized.clear();
  g_LL_resized.clear();

  g_elec = ( m_flavour == kFlavour::ELEC );
  g_muon = ( m_flavour == kFlavour::MUON );
  g_incl = ( m_flavour == kFlavour::INCLUSIVE );

  g_reff = false;
  g_feff = false;
  g_RR   = false;
  g_RF   = false;
  g_FR   = false;
  //g_FF   = false;

}

// ----------------------------------------------------------------------------------------------------------------------

void LHFitter :: readTagAndProbeEff() {

  Info("readTagAndProbeEff()", "Reading histograms with tag and probe efficiencies from input...");

  std::string path     = m_input_path_TP + "Rates.root";
  std::string path_avg = m_input_path_TP + "AvgRates.root";

  TFile *file = TFile::Open(path.c_str());
  if ( !file->IsOpen() ) {
    SysError("readTagAndProbeEff()", "Failed to open ROOT file from path: %s . Aborting", path.c_str() );
    exit(-1);
  }

  TFile *file_avg = TFile::Open(path_avg.c_str());
  if ( !file_avg->IsOpen() ) {
    SysError("readTagAndProbeEff()", "Failed to open ROOT file from path: %s . Aborting", path_avg.c_str() );
    exit(-1);
  }

  std::string filename_rel(""), filename_rel_avg("");
  std::string filename_fel(""), filename_fel_avg("");
  std::string filename_rmu(""), filename_rmu_avg("");
  std::string filename_fmu(""), filename_fmu_avg("");

  filename_rel = filename_rel_avg = "El_ProbePt_Real_Efficiency_observed";
  filename_fel = filename_fel_avg = "El_ProbePt_Fake_Efficiency_observed";
  filename_rmu = filename_rmu_avg = "Mu_ProbePt_Real_Efficiency_observed";
  filename_fmu = filename_fmu_avg = "Mu_ProbePt_Fake_Efficiency_observed";

  TH1D *releff = get_object<TH1D>( *file, filename_rel );
  TH1D *feleff = get_object<TH1D>( *file, filename_fel );
  TH1D *rmueff = get_object<TH1D>( *file, filename_rmu );
  TH1D *fmueff = get_object<TH1D>( *file, filename_fmu );

  // Do not read underflow, but do read overflow!
  //
  for ( int ibin(1); ibin <= releff->GetNbinsX()+1; ++ibin ) {
    m_rel_init.push_back( releff->GetBinContent(ibin) );
  }
  for ( int ibin(1); ibin <= feleff->GetNbinsX()+1; ++ibin ) {
    m_fel_init.push_back( feleff->GetBinContent(ibin) );
  }
  for ( int ibin(1); ibin <= rmueff->GetNbinsX()+1; ++ibin ) {
    m_rmu_init.push_back( rmueff->GetBinContent(ibin) );
  }
  for ( int ibin(1); ibin <= fmueff->GetNbinsX()+1; ++ibin ) {
    m_fmu_init.push_back( fmueff->GetBinContent(ibin) );
  }

  // Save average efficiencies

  TH1D *releff_avg = get_object<TH1D>( *file_avg, filename_rel_avg );
  TH1D *feleff_avg = get_object<TH1D>( *file_avg, filename_fel_avg );
  TH1D *rmueff_avg = get_object<TH1D>( *file_avg, filename_rmu_avg );
  TH1D *fmueff_avg = get_object<TH1D>( *file_avg, filename_fmu_avg );

  m_rel_init_avg = releff_avg->GetBinContent(1);
  m_fel_init_avg = feleff_avg->GetBinContent(1);
  m_rmu_init_avg = rmueff_avg->GetBinContent(1);
  m_fmu_init_avg = fmueff_avg->GetBinContent(1);

}

// ----------------------------------------------------------------------------------------------------------------------

void LHFitter :: getHists() {

  Info("getHists()","Extracting histograms for TT, TL, LT, LL yields from input ROOT files...");

  std::string path("");
  std::string charge("");
  std::vector<std::string> flavour_comb;

  if      ( m_efficiency == kEfficiency::REAL ) charge = "OS";
  else if ( m_efficiency == kEfficiency::FAKE ) charge = "SS";


  if      ( m_flavour == kFlavour::ELEC ) flavour_comb.push_back("ElEl");
  else if ( m_flavour == kFlavour::MUON ) flavour_comb.push_back("MuMu");
  else if ( m_flavour == kFlavour::INCLUSIVE ) {
      flavour_comb.push_back("ElEl");
      flavour_comb.push_back("MuMu");
      flavour_comb.push_back("MuEl");
      flavour_comb.push_back("ElMu");
  }

  for ( const auto& flav : flavour_comb ) {

      for ( const auto& sl : m_obs_selection ) {

	  path = m_input_path_yields + charge + "_" + flav + "_" + sl + "/" + charge + "_" + flav + "_" + sl + "_Lep0Pt_VS_Lep1Pt.root";

	  if ( m_debug ) { Info("getHists()","Reading histogram from:\t %s", path.c_str() ); }

	  TFile *file = TFile::Open(path.c_str());
	  if ( !file->IsOpen() ) {
	      SysError("getHists()", "Failed to open ROOT file from path: %s . Aborting", path.c_str() );
	      exit(-1);
	  }

	  TH2D *hist = get_object<TH2D>( *file, "observed" );

	  // -) Do ( !prompt & charge flip ) subtraction in OS
	  // -) Do ( prompt & charge flip ) subtraction in SS
	  //
	  if  ( m_doSubtraction ) {

	      Info("getHists()", "Subtracting bkgs to data...");

	      TH2D *hist_to_sub = get_object<TH2D>( *file, "expected" );
	      hist->Add(hist_to_sub, -1.0);

	      // Set bin content to 0 if subtraction gives negative yield
	      //
	      for ( int ibiny(0); ibiny < hist->GetNbinsX()+2; ++ibiny ) {
		  for ( int ibinx(0); ibinx < hist->GetNbinsX()+2; ++ibinx ) {
		      if ( hist->GetBinContent( hist->GetBin(ibinx,ibiny)  ) < 0 ) { hist->SetBinContent( hist->GetBin(ibinx,ibiny), 0.0); }
		  }
	      }
	  }

	  std::string new_name = charge + "_" + flav + "_" + sl;

	  if ( m_debug ) { Info("getHists()","Storing histogram w/ name:\t %s for later use", new_name.c_str() ); }

	  hist->SetName(new_name.c_str());

	  hist->SetDirectory(0);

	  if ( m_doRebinning ) {

	      Info("getHists()","Rebinning histogram...");

	      TH2D* htemp = dynamic_cast<TH2D*>( hist->Clone() );

	      if ( m_nBinGroup > 1 ) {
		  Info("getHists()","Using fixed bin size, grouping %i bins", m_nBinGroup );
		  hist = dynamic_cast<TH2D*>( htemp->Rebin2D( m_nBinGroup, m_nBinGroup, htemp->GetName() ) );
	      } else {
		  Info("getHists()","Using variable bin size:");
		  std::cout << "new nbins: " << m_newNBins << " - bin low edges: " << std::endl;
		  for ( int ibin(0); ibin < m_newNBins+1; ++ibin ) {
		      std::cout << m_newBins[ibin] << " ";
		  }
		  std::cout << std::endl;

		  // Need this trick to create 2D rebinned histogram w/ variable bin size
		  TH2D *hrebinned = new TH2D("rebinned",hist->GetTitle(), m_newNBins, m_newBins, m_newNBins, m_newBins );
		  hrebinned->SetName(hist->GetName());
		  hrebinned->SetDirectory(0);
		  TAxis *xaxis = hist->GetXaxis();
		  TAxis *yaxis = hist->GetYaxis();
		  for ( int ibiny(0); ibiny < hist->GetNbinsY()+2; ++ibiny ) {
		      for ( int ibinx(0); ibinx < hist->GetNbinsX()+2; ++ibinx ) {
			  hrebinned->Fill( xaxis->GetBinCenter(ibinx), yaxis->GetBinCenter(ibiny), hist->GetBinContent(ibinx,ibiny) );
		      }
		  }
		  m_histograms.push_back(hrebinned);
		  continue;
	      }

	  }

	  m_histograms.push_back(hist);

      }
  }

  m_nPtBins_Linear  = ( m_histograms.at(0) )->GetNbinsX() + 1;
  m_nPtBins_Squared = areaGrid( m_nPtBins_Linear );

  // set it as a global variable
  //
  g_nPtBins_Squared = m_nPtBins_Squared;

  if ( m_debug ) { Info("getHists()","Reading observed histograms for TT, TL, LT, LL yields:"); }

  // UGLYYYYYYYYYY
  int idx(0);
  while ( idx < (m_nPtBins_Linear + 1) * (m_nPtBins_Linear + 1) ) {
    m_TelTel.push_back(0.0);
    m_TelLel.push_back(0.0);
    m_LelTel.push_back(0.0);
    m_LelLel.push_back(0.0);

    m_TmuTmu.push_back(0.0);
    m_TmuLmu.push_back(0.0);
    m_LmuTmu.push_back(0.0);
    m_LmuLmu.push_back(0.0);

    m_TmuTel.push_back(0.0);
    m_TmuLel.push_back(0.0);
    m_LmuTel.push_back(0.0);
    m_LmuLel.push_back(0.0);

    m_TelTmu.push_back(0.0);
    m_TelLmu.push_back(0.0);
    m_LelTmu.push_back(0.0);
    m_LelLmu.push_back(0.0);

    ++idx;
  }

  for ( auto hist : m_histograms ) {

    // To get overflow as well (but no underflow)
    //
    int firstxbin = 1;
    int firstybin = 1;
    int lastxbin  = m_nPtBins_Linear;
    int lastybin  = m_nPtBins_Linear;

    if ( m_debug ) { std::cout << "\t" << hist->GetName() << " - Integral: " << hist->Integral(firstxbin,lastxbin,firstybin,lastybin) << std::endl; }

    std::string charge("");
    if      ( m_efficiency == kEfficiency::REAL ) charge = "OS";
    else if ( m_efficiency == kEfficiency::FAKE ) charge = "SS";

    std::string TelTel_name = charge + "_ElEl_TT";
    std::string TelLel_name = charge + "_ElEl_TL";
    std::string LelTel_name = charge + "_ElEl_LT";
    std::string LelLel_name = charge + "_ElEl_LL";

    std::string TmuTmu_name = charge + "_MuMu_TT";
    std::string TmuLmu_name = charge + "_MuMu_TL";
    std::string LmuTmu_name = charge + "_MuMu_LT";
    std::string LmuLmu_name = charge + "_MuMu_LL";

    std::string TmuTel_name = charge + "_MuEl_TT";
    std::string TmuLel_name = charge + "_MuEl_TL";
    std::string LmuTel_name = charge + "_MuEl_LT";
    std::string LmuLel_name = charge + "_MuEl_LL";

    std::string TelTmu_name = charge + "_ElMu_TT";
    std::string TelLmu_name = charge + "_ElMu_TL";
    std::string LelTmu_name = charge + "_ElMu_LT";
    std::string LelLmu_name = charge + "_ElMu_LL";

    if ( strcmp( hist->GetName(), TelTel_name.c_str() ) == 0 ) {
      for ( int ibiny(0); ibiny <= m_nPtBins_Linear; ++ibiny ) {
        for ( int ibinx(0); ibinx <= m_nPtBins_Linear; ++ibinx ) {
          if ( m_verbose ) { std::cout << "(" << ibinx << "," << ibiny << ") - global bin: " << hist->GetBin(ibinx,ibiny) << std::endl; }
          m_TelTel.at( hist->GetBin(ibinx,ibiny) )  = hist->GetBinContent( hist->GetBin(ibinx,ibiny) );
        }
      }
    } else if ( strcmp( hist->GetName(), TelLel_name.c_str() ) == 0 ) {
      for ( int ibiny(0); ibiny <= m_nPtBins_Linear; ++ibiny ) {
        for ( int ibinx(0); ibinx <= m_nPtBins_Linear; ++ibinx ) {
          if ( m_verbose ) { std::cout << "(" << ibinx << "," << ibiny << ") - global bin: " << hist->GetBin(ibinx,ibiny) << std::endl; }
          m_TelLel.at( hist->GetBin(ibinx,ibiny) )  = hist->GetBinContent( hist->GetBin(ibinx,ibiny) );
        }
      }
    } else if ( strcmp( hist->GetName(), LelTel_name.c_str() ) == 0 ) {
      for ( int ibiny(0); ibiny <= m_nPtBins_Linear; ++ibiny ) {
        for ( int ibinx(0); ibinx <= m_nPtBins_Linear; ++ibinx ) {
          if ( m_verbose ) { std::cout << "(" << ibinx << "," << ibiny << ") - global bin: " << hist->GetBin(ibinx,ibiny) << std::endl; }
          m_LelTel.at( hist->GetBin(ibinx,ibiny) )  = hist->GetBinContent( hist->GetBin(ibinx,ibiny) );
        }
      }
    } else if ( strcmp( hist->GetName(), LelLel_name.c_str() ) == 0 ) {
      for ( int ibiny(0); ibiny <= m_nPtBins_Linear; ++ibiny ) {
        for ( int ibinx(0); ibinx <= m_nPtBins_Linear; ++ibinx ) {
          if ( m_verbose ) { std::cout << "(" << ibinx << "," << ibiny << ") - global bin: " << hist->GetBin(ibinx,ibiny) << std::endl; }
          m_LelLel.at( hist->GetBin(ibinx,ibiny) )  = hist->GetBinContent( hist->GetBin(ibinx,ibiny) );
        }
      }
    }

    if ( strcmp( hist->GetName(), TmuTmu_name.c_str() ) == 0 ) {
      for ( int ibiny(0); ibiny <= m_nPtBins_Linear; ++ibiny ) {
        for ( int ibinx(0); ibinx <= m_nPtBins_Linear; ++ibinx ) {
          if ( m_verbose ) { std::cout << "(" << ibinx << "," << ibiny << ") - global bin: " << hist->GetBin(ibinx,ibiny) << std::endl; }
          m_TmuTmu.at( hist->GetBin(ibinx,ibiny) )  = hist->GetBinContent( hist->GetBin(ibinx,ibiny) );
        }
      }
    } else if ( strcmp( hist->GetName(), TmuLmu_name.c_str() ) == 0 ) {
      for ( int ibiny(0); ibiny <= m_nPtBins_Linear; ++ibiny ) {
        for ( int ibinx(0); ibinx <= m_nPtBins_Linear; ++ibinx ) {
          if ( m_verbose ) { std::cout << "(" << ibinx << "," << ibiny << ") - global bin: " << hist->GetBin(ibinx,ibiny) << std::endl; }
          m_TmuLmu.at( hist->GetBin(ibinx,ibiny) )  = hist->GetBinContent( hist->GetBin(ibinx,ibiny) );
        }
      }
    } else if ( strcmp( hist->GetName(), LmuTmu_name.c_str() ) == 0 ) {
      for ( int ibiny(0); ibiny <= m_nPtBins_Linear; ++ibiny ) {
        for ( int ibinx(0); ibinx <= m_nPtBins_Linear; ++ibinx ) {
          if ( m_verbose ) { std::cout << "(" << ibinx << "," << ibiny << ") - global bin: " << hist->GetBin(ibinx,ibiny) << std::endl; }
          m_LmuTmu.at( hist->GetBin(ibinx,ibiny) )  = hist->GetBinContent( hist->GetBin(ibinx,ibiny) );
        }
      }
    } else if ( strcmp( hist->GetName(), LmuLmu_name.c_str() ) == 0 ) {
      for ( int ibiny(0); ibiny <= m_nPtBins_Linear; ++ibiny ) {
        for ( int ibinx(0); ibinx <= m_nPtBins_Linear; ++ibinx ) {
          if ( m_verbose ) { std::cout << "(" << ibinx << "," << ibiny << ") - global bin: " << hist->GetBin(ibinx,ibiny) << std::endl; }
          m_LmuLmu.at( hist->GetBin(ibinx,ibiny) )  = hist->GetBinContent( hist->GetBin(ibinx,ibiny) );
        }
      }
    }

    if ( strcmp( hist->GetName(), TmuTel_name.c_str() ) == 0 ) {
      for ( int ibiny(0); ibiny <= m_nPtBins_Linear; ++ibiny ) {
        for ( int ibinx(0); ibinx <= m_nPtBins_Linear; ++ibinx ) {
          if ( m_verbose ) { std::cout << "(" << ibinx << "," << ibiny << ") - global bin: " << hist->GetBin(ibinx,ibiny) << std::endl; }
          m_TmuTel.at( hist->GetBin(ibinx,ibiny) )  = hist->GetBinContent( hist->GetBin(ibinx,ibiny) );
        }
      }
    } else if ( strcmp( hist->GetName(), TmuLel_name.c_str() ) == 0 ) {
      for ( int ibiny(0); ibiny <= m_nPtBins_Linear; ++ibiny ) {
        for ( int ibinx(0); ibinx <= m_nPtBins_Linear; ++ibinx ) {
          if ( m_verbose ) { std::cout << "(" << ibinx << "," << ibiny << ") - global bin: " << hist->GetBin(ibinx,ibiny) << std::endl; }
          m_TmuLel.at( hist->GetBin(ibinx,ibiny) )  = hist->GetBinContent( hist->GetBin(ibinx,ibiny) );
        }
      }
    } else if ( strcmp( hist->GetName(), LmuTel_name.c_str() ) == 0 ) {
      for ( int ibiny(0); ibiny <= m_nPtBins_Linear; ++ibiny ) {
        for ( int ibinx(0); ibinx <= m_nPtBins_Linear; ++ibinx ) {
          if ( m_verbose ) { std::cout << "(" << ibinx << "," << ibiny << ") - global bin: " << hist->GetBin(ibinx,ibiny) << std::endl; }
          m_LmuTel.at( hist->GetBin(ibinx,ibiny) )  = hist->GetBinContent( hist->GetBin(ibinx,ibiny) );
        }
      }
    } else if ( strcmp( hist->GetName(), LmuLel_name.c_str() ) == 0 ) {
      for ( int ibiny(0); ibiny <= m_nPtBins_Linear; ++ibiny ) {
        for ( int ibinx(0); ibinx <= m_nPtBins_Linear; ++ibinx ) {
          if ( m_verbose ) { std::cout << "(" << ibinx << "," << ibiny << ") - global bin: " << hist->GetBin(ibinx,ibiny) << std::endl; }
          m_LmuLel.at( hist->GetBin(ibinx,ibiny) )  = hist->GetBinContent( hist->GetBin(ibinx,ibiny) );
        }
      }
    }

    if ( strcmp( hist->GetName(), TelTmu_name.c_str() ) == 0 ) {
      for ( int ibiny(0); ibiny <= m_nPtBins_Linear; ++ibiny ) {
        for ( int ibinx(0); ibinx <= m_nPtBins_Linear; ++ibinx ) {
          if ( m_verbose ) { std::cout << "(" << ibinx << "," << ibiny << ") - global bin: " << hist->GetBin(ibinx,ibiny) << std::endl; }
          m_TelTmu.at( hist->GetBin(ibinx,ibiny) )  = hist->GetBinContent( hist->GetBin(ibinx,ibiny) );
        }
      }
    } else if ( strcmp( hist->GetName(), TelLmu_name.c_str() ) == 0 ) {
      for ( int ibiny(0); ibiny <= m_nPtBins_Linear; ++ibiny ) {
        for ( int ibinx(0); ibinx <= m_nPtBins_Linear; ++ibinx ) {
          if ( m_verbose ) { std::cout << "(" << ibinx << "," << ibiny << ") - global bin: " << hist->GetBin(ibinx,ibiny) << std::endl; }
          m_TelLmu.at( hist->GetBin(ibinx,ibiny) )  = hist->GetBinContent( hist->GetBin(ibinx,ibiny) );
        }
      }
    } else if ( strcmp( hist->GetName(), LelTmu_name.c_str() ) == 0 ) {
      for ( int ibiny(0); ibiny <= m_nPtBins_Linear; ++ibiny ) {
        for ( int ibinx(0); ibinx <= m_nPtBins_Linear; ++ibinx ) {
          if ( m_verbose ) { std::cout << "(" << ibinx << "," << ibiny << ") - global bin: " << hist->GetBin(ibinx,ibiny) << std::endl; }
          m_LelTmu.at( hist->GetBin(ibinx,ibiny) )  = hist->GetBinContent( hist->GetBin(ibinx,ibiny) );
        }
      }
    } else if ( strcmp( hist->GetName(), LelLmu_name.c_str() ) == 0 ) {
      for ( int ibiny(0); ibiny <= m_nPtBins_Linear; ++ibiny ) {
        for ( int ibinx(0); ibinx <= m_nPtBins_Linear; ++ibinx ) {
          if ( m_verbose ) { std::cout << "(" << ibinx << "," << ibiny << ") - global bin: " << hist->GetBin(ibinx,ibiny) << std::endl; }
          m_LelLmu.at( hist->GetBin(ibinx,ibiny) )  = hist->GetBinContent( hist->GetBin(ibinx,ibiny) );
        }
      }
    }

  }

}

// ----------------------------------------------------------------------------------------------------------------------

void LHFitter :: getEducatedGuess( ) {

  Info("getEducatedGuess()","Getting initial values for fit parameters...");

  // TEMP - hardcode efficiency
  //double r =  0.65;
  //double f = 0.172;

  //for ( int idx(0); idx < nPtBins_Linear-1; ++idx ) {
  //  m_r_init.push_back(r);
  //  m_f_init.push_back(f);
  //}

  // Read tag-and-probe efficiencies from input file
  //
  this->readTagAndProbeEff();

  // loop over 2D pT histogram, and depending on the pT value of the leading/subleading lepton,
  // read the corresponding tag-and-probe efficiency, read the TT, TL...yields per bin (set previously in the vectors),
  // and finally compute nRR, nRF...in every bin

  // Skip the (0,j) and (i,0) bins --> they are underflow
  // Skip the (i,j) bins where i < j (empty by construction)

  double r1el(-1.0), r2el(-1.0);
  double f1el(-1.0), f2el(-1.0);
  double r1mu(-1.0), r2mu(-1.0);
  double f1mu(-1.0), f2mu(-1.0);

  double nTelTel(0.0), nTelLel(0.0), nLelTel(0.0), nLelLel(0.0);
  double nTmuTmu(0.0), nTmuLmu(0.0), nLmuTmu(0.0), nLmuLmu(0.0);
  double nTmuTel(0.0), nTmuLel(0.0), nLmuTel(0.0), nLmuLel(0.0);
  double nTelTmu(0.0), nTelLmu(0.0), nLelTmu(0.0), nLelLmu(0.0);

  double RelRel_default(1e-3), RelFel_default(1e-3), FelRel_default(1e-3), FelFel_default(1e-3);
  double RmuRmu_default(1e-3), RmuFmu_default(1e-3), FmuRmu_default(1e-3), FmuFmu_default(1e-3);
  double RmuRel_default(1e-3), RmuFel_default(1e-3), FmuRel_default(1e-3), FmuFel_default(1e-3);
  double RelRmu_default(1e-3), RelFmu_default(1e-3), FelRmu_default(1e-3), FelFmu_default(1e-3);

  // Drop tail of m_r_init, m_f_init vectors if their size is greater than the actual number of bins
  while ( m_rel_init.size() > m_nPtBins_Linear ) { m_rel_init.pop_back(); }
  while ( m_fel_init.size() > m_nPtBins_Linear ) { m_fel_init.pop_back(); }
  while ( m_rmu_init.size() > m_nPtBins_Linear ) { m_rmu_init.pop_back(); }
  while ( m_fmu_init.size() > m_nPtBins_Linear ) { m_fmu_init.pop_back(); }

  // Add elements to tail of vector ( pushing back the average efficiency ) if size is smaller than the actual number of bins
  while ( m_rel_init.size() < m_nPtBins_Linear ) { m_rel_init.push_back( m_rel_init_avg ); }
  while ( m_fel_init.size() < m_nPtBins_Linear ) { m_fel_init.push_back( m_fel_init_avg ); }
  while ( m_rmu_init.size() < m_nPtBins_Linear ) { m_rmu_init.push_back( m_rmu_init_avg ); }
  while ( m_fmu_init.size() < m_nPtBins_Linear ) { m_fmu_init.push_back( m_fmu_init_avg ); }


  std::cout << "" << std::endl;
  Info("getEducatedGuess()","===> Will be using average f to determine initial guesses for RR, RF, FR, FF yields..." );
  Info("getEducatedGuess()","<fel> = %.2f", m_fel_init_avg );
  Info("getEducatedGuess()","<fmu> = %.2f", m_fmu_init_avg );

  if ( m_doRebinning ) {
      std::cout << "" << std::endl;
      Info("getEducatedGuess()","REBINNING ACTIVATED!" );
      Info("getEducatedGuess()","===> Will be using ALSO average r to determine initial guesses for RR, RF, FR, FF yields..." );
      Info("getEducatedGuess()","<rel> = %.2f", m_rel_init_avg );
      Info("getEducatedGuess()","<rmu> = %.2f", m_rmu_init_avg );
      for ( int ibin(0); ibin < m_nPtBins_Linear; ++ibin ) {
        m_rel_init.at(ibin) = m_rel_init_avg;
        m_rel_init.at(ibin) = m_rel_init_avg;
        m_fmu_init.at(ibin) = m_fmu_init_avg;
        m_fmu_init.at(ibin) = m_fmu_init_avg;
      }
  }

  int glob_bin_idx(-1);
  for ( int ibiny(1); ibiny <= m_nPtBins_Linear; ++ibiny ) {

    r2el = m_rel_init.at(ibiny-1);
    f2el = m_fel_init_avg;
    r2mu = m_rmu_init.at(ibiny-1);
    f2mu = m_fmu_init_avg;

    for ( int ibinx(1); ibinx <= m_nPtBins_Linear; ++ibinx ) {

      r1el = m_rel_init.at(ibinx-1);
      f1el = m_fel_init_avg;
      r1mu = m_rmu_init.at(ibinx-1);
      f1mu = m_fmu_init_avg;

      // Skip the above-diagonal elements
      //
      if ( ibiny > ibinx ) { continue; }

      glob_bin_idx = m_histograms.at(0)->GetBin(ibinx,ibiny); // can use any of the input histograms: take the first by default

      nTelTel = m_TelTel.at(glob_bin_idx);
      nTelLel = m_TelLel.at(glob_bin_idx);
      nLelTel = m_LelTel.at(glob_bin_idx);
      nLelLel = m_LelLel.at(glob_bin_idx);

      nTmuTmu = m_TmuTmu.at(glob_bin_idx);
      nTmuLmu = m_TmuLmu.at(glob_bin_idx);
      nLmuTmu = m_LmuTmu.at(glob_bin_idx);
      nLmuLmu = m_LmuLmu.at(glob_bin_idx);

      nTmuTel = m_TmuTel.at(glob_bin_idx);
      nTmuLel = m_TmuLel.at(glob_bin_idx);
      nLmuTel = m_LmuTel.at(glob_bin_idx);
      nLmuLel = m_LmuLel.at(glob_bin_idx);

      nTelTmu = m_TelTmu.at(glob_bin_idx);
      nTelLmu = m_TelLmu.at(glob_bin_idx);
      nLelTmu = m_LelTmu.at(glob_bin_idx);
      nLelLmu = m_LelLmu.at(glob_bin_idx);

      if ( m_verbose ) {
        std::cout << "global bin: " << glob_bin_idx << std::endl;
        std::cout << "nTelTel: " << nTelTel << std::endl;
        std::cout << "nTelLel: " << nTelLel << std::endl;
        std::cout << "nLelTel: " << nLelTel << std::endl;
        std::cout << "nLelLel: " << nLelLel << std::endl;

        std::cout << "nTmuTmu: " << nTmuTmu << std::endl;
        std::cout << "nTmuLmu: " << nTmuLmu << std::endl;
        std::cout << "nLmuTmu: " << nLmuTmu << std::endl;
        std::cout << "nLmuLmu: " << nLmuLmu << std::endl;

        std::cout << "nTmuTel: " << nTmuTel << std::endl;
        std::cout << "nTmuLel: " << nTmuLel << std::endl;
        std::cout << "nLmuTel: " << nLmuTel << std::endl;
        std::cout << "nLmuLel: " << nLmuLel << std::endl;

        std::cout << "nTelTmu: " << nTelTmu << std::endl;
        std::cout << "nTelLmu: " << nTelLmu << std::endl;
        std::cout << "nLelTmu: " << nLelTmu << std::endl;
        std::cout << "nLelLmu: " << nLelLmu << std::endl;

        std::cout << "r1el: " << r1el << std::endl;
        std::cout << "r2el: " << r2el << std::endl;
        std::cout << "f1el: " << f1el << std::endl;
        std::cout << "f2el: " << f2el << std::endl;

        std::cout << "r1mu: " << r1mu << std::endl;
        std::cout << "r2mu: " << r2mu << std::endl;
        std::cout << "f1mu: " << f1mu << std::endl;
        std::cout << "f2mu: " << f2mu << std::endl;

        std::cout << "" << std::endl;
      }

      double alpha_elel = ( r1el - f1el ) * ( r2el - f2el );
      double alpha_mumu = ( r1mu - f1mu ) * ( r2mu - f2mu );
      double alpha_muel = ( r1mu - f1mu ) * ( r2el - f2el );
      double alpha_elmu = ( r1el - f1el ) * ( r2mu - f2mu );

      double RelRel = ( 1.0 / alpha_elel ) * ( ( 1 - f1el ) * ( 1 - f2el ) * nTT + ( f1el - 1 ) * f2el * nTL + ( f2el - 1 ) * f1el * nLT + f1el * f2el * nLL );
      double RelFel = ( 1.0 / alpha_elel ) * ( ( f1el - 1 ) * ( 1 - r2el ) * nTT + ( 1 - f1el ) * r2el * nTL + ( 1 - r2el ) * f1el * nLT - f1el * r2el * nLL );
      double FelRel = ( 1.0 / alpha_elel ) * ( ( r1el - 1 ) * ( 1 - f2el ) * nTT + ( 1 - r1el ) * f2el * nTL + ( 1 - f2el ) * r1el * nLT - r1el * f2el * nLL );
      //double FelFel = ( 1.0 / alpha_elel ) * ( ( 1 - r1el ) * ( 1 - r2el ) * nTT + ( r1el - 1 ) * r2el * nTL + ( r2el - 1 ) * r1el * nLT + r1el * r2el * nLL );
      double RmuRmu = ( 1.0 / alpha_mumu ) * ( ( 1 - f1mu ) * ( 1 - f2mu ) * nTT + ( f1mu - 1 ) * f2mu * nTL + ( f2mu - 1 ) * f1mu * nLT + f1mu * f2mu * nLL );
      double RmuFmu = ( 1.0 / alpha_mumu ) * ( ( f1mu - 1 ) * ( 1 - r2mu ) * nTT + ( 1 - f1mu ) * r2mu * nTL + ( 1 - r2mu ) * f1mu * nLT - f1mu * r2mu * nLL );
      double FmuRmu = ( 1.0 / alpha_mumu ) * ( ( r1mu - 1 ) * ( 1 - f2mu ) * nTT + ( 1 - r1mu ) * f2mu * nTL + ( 1 - f2mu ) * r1mu * nLT - r1mu * f2mu * nLL );
      //double FmuFmu = ( 1.0 / alpha_mumu ) * ( ( 1 - r1mu ) * ( 1 - r2mu ) * nTT + ( r1mu - 1 ) * r2mu * nTL + ( r2mu - 1 ) * r1mu * nLT + r1mu * r2mu * nLL );
      double RmuRel = ( 1.0 / alpha_muel ) * ( ( 1 - f1mu ) * ( 1 - f2el ) * nTT + ( f1mu - 1 ) * f2el * nTL + ( f2el - 1 ) * f1mu * nLT + f1mu * f2el * nLL );
      double RmuFel = ( 1.0 / alpha_muel ) * ( ( f1mu - 1 ) * ( 1 - r2el ) * nTT + ( 1 - f1mu ) * r2el * nTL + ( 1 - r2el ) * f1mu * nLT - f1mu * r2el * nLL );
      double FmuRel = ( 1.0 / alpha_muel ) * ( ( r1mu - 1 ) * ( 1 - f2el ) * nTT + ( 1 - r1mu ) * f2el * nTL + ( 1 - f2el ) * r1mu * nLT - r1mu * f2el * nLL );
      //double FmuFel = ( 1.0 / alpha_muel ) * ( ( 1 - r1mu ) * ( 1 - r2el ) * nTT + ( r1mu - 1 ) * r2el * nTL + ( r2el - 1 ) * r1mu * nLT + r1mu * r2el * nLL );
      double RelRmu = ( 1.0 / alpha_elmu ) * ( ( 1 - f1el ) * ( 1 - f2mu ) * nTT + ( f1el - 1 ) * f2mu * nTL + ( f2mu - 1 ) * f1el * nLT + f1el * f2mu * nLL );
      double RelFmu = ( 1.0 / alpha_elmu ) * ( ( f1el - 1 ) * ( 1 - r2mu ) * nTT + ( 1 - f1el ) * r2mu * nTL + ( 1 - r2mu ) * f1el * nLT - f1el * r2mu * nLL );
      double FelRmu = ( 1.0 / alpha_elmu ) * ( ( r1el - 1 ) * ( 1 - f2mu ) * nTT + ( 1 - r1el ) * f2mu * nTL + ( 1 - f2mu ) * r1el * nLT - r1el * f2mu * nLL );
      //double FelFmu = ( 1.0 / alpha_elmu ) * ( ( 1 - r1el ) * ( 1 - r2mu ) * nTT + ( r1el - 1 ) * r2mu * nTL + ( r2mu - 1 ) * r1el * nLT + r1el * r2mu * nLL );

      // Reset yields to zero if unphisically negative
      // (Actually to 1 to avoid warnings b/c of lower physical limit set on yields...)
      //
      if ( RelRel >= 0.0 ) { m_RelRel_init.push_back( RelRel ); } else { m_RelRel_init.push_back( 1.0 ); }
      if ( RelFel >= 0.0 ) { m_RelFel_init.push_back( RelFel ); } else { m_RelFel_init.push_back( 1.0 ); }
      if ( FelRel >= 0.0 ) { m_FelRel_init.push_back( FelRel ); } else { m_FelRel_init.push_back( 1.0 ); }
      //if ( FelFel >= 0.0 ) { m_FelFel_init.push_back( FelFel ); } else { m_FelFel_init.push_back( 1.0 ); }
      if ( RmuRmu >= 0.0 ) { m_RmuRmu_init.push_back( RmuRmu ); } else { m_RmuRmu_init.push_back( 1.0 ); }
      if ( RmuFmu >= 0.0 ) { m_RmuFmu_init.push_back( RmuFmu ); } else { m_RmuFmu_init.push_back( 1.0 ); }
      if ( FmuRmu >= 0.0 ) { m_FmuRmu_init.push_back( FmuRmu ); } else { m_FmuRmu_init.push_back( 1.0 ); }
      //if ( FmuFmu >= 0.0 ) { m_FmuFmu_init.push_back( FmuFmu ); } else { m_FmuFmu_init.push_back( 1.0 ); }
      if ( RmuRel >= 0.0 ) { m_RmuRel_init.push_back( RmuRel ); } else { m_RmuRel_init.push_back( 1.0 ); }
      if ( RmuFel >= 0.0 ) { m_RmuFel_init.push_back( RmuFel ); } else { m_RmuFel_init.push_back( 1.0 ); }
      if ( FmuRel >= 0.0 ) { m_FmuRel_init.push_back( FmuRel ); } else { m_FmuRel_init.push_back( 1.0 ); }
      //if ( FmuFel >= 0.0 ) { m_FmuFel_init.push_back( FmuFel ); } else { m_FmuFel_init.push_back( 1.0 ); }
      if ( RelRmu >= 0.0 ) { m_RelRmu_init.push_back( RelRmu ); } else { m_RelRmu_init.push_back( 1.0 ); }
      if ( RelFmu >= 0.0 ) { m_RelFmu_init.push_back( RelFmu ); } else { m_RelFmu_init.push_back( 1.0 ); }
      if ( FelRmu >= 0.0 ) { m_FelRmu_init.push_back( FelRmu ); } else { m_FelRmu_init.push_back( 1.0 ); }
      //if ( FelFmu >= 0.0 ) { m_FelFmu_init.push_back( FelFmu ); } else { m_FelFmu_init.push_back( 1.0 ); }

      // Copy only relevant bins for observed yields into these containers
      // (will be the ones used in the likelihood)
      //
      g_TelTel_resized.push_back( nTelTel );
      g_TelLel_resized.push_back( nTelLel );
      g_LelTel_resized.push_back( nLelTel );
      g_LelLel_resized.push_back( nLelLel );

      g_TmuTmu_resized.push_back( nTmuTmu );
      g_TmuLmu_resized.push_back( nTmuLmu );
      g_LmuTmu_resized.push_back( nLmuTmu );
      g_LmuLmu_resized.push_back( nLmuLmu );

      g_TmuTel_resized.push_back( nTmuTel );
      g_TmuLel_resized.push_back( nTmuLel );
      g_LmuTel_resized.push_back( nLmuTel );
      g_LmuLel_resized.push_back( nLmuLel );

      g_TelTmu_resized.push_back( nTelTmu );
      g_TelLmu_resized.push_back( nTelLmu );
      g_LelTmu_resized.push_back( nLelTmu );
      g_LelLmu_resized.push_back( nLelLmu );

    }
  }

}

// ----------------------------------------------------------------------------------------------------------------------

void LHFitter :: getParametersAndErrors() {

  Info("getParametersAndErrors()","Retrieveing fitted parameters and their errors...");

  int offset(0); // needed for dealing with parameter offsets (TMinuit can accept only one huge array of parameters...)
  int param_idx(0);

  double globcc;

  // --------------------
  // Get errors for r
  // --------------------

  if ( m_efficiency == kEfficiency::REAL ) {

    for ( auto idx(0); idx < m_r_errs.size(); ++idx ) {
       param_idx = offset + idx;
       m_myFitter->GetParameter( param_idx, m_r_vals.at(idx), std::get<2>(m_r_errs.at(idx)) );
       m_myFitter->mnerrs( param_idx, std::get<0>(m_r_errs.at(idx)), std::get<1>(m_r_errs.at(idx)), std::get<2>(m_r_errs.at(idx)), globcc );
    }

    for ( int ibiny(1); ibiny <= m_nPtBins_Linear; ++ibiny ) {
      for ( int ibinx(1); ibinx <= m_nPtBins_Linear; ++ibinx ) {
        if ( ibiny > ibinx ) { continue; }
	if ( m_flavour == kFlavour::ELEC ) {
          g_fitted_r1_el.push_back( m_r_vals.at(ibinx-1) );
          g_fitted_r2_el.push_back( m_r_vals.at(ibiny-1) );
	}
	if ( m_flavour == kFlavour::MUON ) {
          g_fitted_r1_mu.push_back( m_r_vals.at(ibinx-1) );
          g_fitted_r2_mu.push_back( m_r_vals.at(ibiny-1) );
	}
      }
    }

    // Set the offset for total parameter index
    //
    offset += m_nPtBins_Linear;
  }

  // --------------------
  // Get errors for f
  // --------------------

  if ( m_efficiency == kEfficiency::FAKE ) {

    for ( auto idx(0); idx < m_f_errs.size(); ++idx ) {
       param_idx = offset + idx;
       m_myFitter->GetParameter( param_idx, m_f_vals.at(idx), std::get<2>(m_f_errs.at(idx)) );
       m_myFitter->mnerrs( param_idx, std::get<0>(m_f_errs.at(idx)), std::get<1>(m_f_errs.at(idx)), std::get<2>(m_f_errs.at(idx)), globcc );
    }
    // Set the offset for total parameter index
    //
    offset += m_nPtBins_Linear;
  }

  // ---------------------
  // Get errors for RR
  // ---------------------

  if ( m_efficiency == kEfficiency::REAL ) {

    for ( auto idx(0); idx < m_RR_errs.size(); ++idx ) {
    	param_idx = offset + idx;
        m_myFitter->GetParameter( param_idx, m_RR_vals.at(idx), std::get<2>(m_RR_errs.at(idx)) );
        m_myFitter->mnerrs( param_idx, std::get<0>(m_RR_errs.at(idx)), std::get<1>(m_RR_errs.at(idx)), std::get<2>(m_RR_errs.at(idx)), globcc );
    }
    // Set the offset for total parameter index
    //
    offset += m_nPtBins_Squared;
  }

  // ---------------------
  // Get errors for RF
  // ---------------------

  if ( m_efficiency == kEfficiency::FAKE ) {

    for ( auto idx(0); idx < m_RF_errs.size(); ++idx ) {
    	param_idx = offset + idx;
        m_myFitter->GetParameter( param_idx, m_RF_vals.at(idx), std::get<2>(m_RF_errs.at(idx)) );
        m_myFitter->mnerrs( param_idx, std::get<0>(m_RF_errs.at(idx)), std::get<1>(m_RF_errs.at(idx)), std::get<2>(m_RF_errs.at(idx)), globcc );
    }
    // Set the offset for total parameter index
    //
    offset += m_nPtBins_Squared;
  }

  // ---------------------
  // Get errors for FR
  // ---------------------

  if ( m_efficiency == kEfficiency::FAKE ) {

    for ( auto idx(0); idx < m_FR_errs.size(); ++idx ) {
    	param_idx = offset + idx;
        m_myFitter->GetParameter( param_idx, m_FR_vals.at(idx), std::get<2>(m_FR_errs.at(idx)) );
        m_myFitter->mnerrs( param_idx, std::get<0>(m_FR_errs.at(idx)), std::get<1>(m_FR_errs.at(idx)), std::get<2>(m_FR_errs.at(idx)), globcc );
    }
    // Set the offset for total parameter index
    //
    offset += m_nPtBins_Squared;
  }

  // ---------------------
  // Get errors for FF
  // ---------------------

  /*
  if ( m_efficiency == kEfficiency::FAKE ) {

    for ( auto idx(0); idx < m_FF_errs.size(); ++idx ) {
    	param_idx = offset + idx;
        m_myFitter->GetParameter( param_idx, m_FF_vals.at(idx), std::get<2>(m_FF_errs.at(idx)) );
        m_myFitter->mnerrs( param_idx, std::get<0>(m_FF_errs.at(idx)), std::get<1>(m_FF_errs.at(idx)), std::get<2>(m_FF_errs.at(idx)), globcc );
    }
    // Set the offset for total parameter index
    //
    offset += m_nPtBins_Squared;
  }
  */
}

// ----------------------------------------------------------------------------------------------------------------------

void  LHFitter :: saveEfficiencies() {

  Info("saveEfficiencies()","Saving fitted efficiency to output...");

  //TH1::ResetBit(TH1::kCanRebin);

  std::string outfilename("LH_efficiencies");

  if      ( m_efficiency == kEfficiency::REAL ) { outfilename += "_real"; }
  else if ( m_efficiency == kEfficiency::FAKE ) { outfilename += "_fake"; }

  if      ( m_flavour == kFlavour::MUON ) { outfilename += "_mu"; }
  else if ( m_flavour == kFlavour::ELEC ) { outfilename += "_el"; }

  std::string rootfilename = outfilename + ".root";
  TFile outfile(rootfilename.c_str(),"RECREATE");

  std::string txtfilename = outfilename + ".txt";
  std::ofstream outtextfile(txtfilename.c_str(), std::ios::trunc);
  outtextfile << "Efficiencies for FF amd Matrix Method from LH fit \n";

  // --------------------
  // real efficiency
  // --------------------

  if ( m_efficiency == kEfficiency::REAL ) {

    TH1D *r_hist(nullptr);
    if ( m_doRebinning && m_useVariableBins ) {
	r_hist = new TH1D( "r_hist", "real efficiency", m_newNBins, m_newBins );
    } else {
      double rmin = ( m_histograms.at(0) )->GetXaxis()->GetBinLowEdge(1);
      double rmax = ( m_histograms.at(0) )->GetXaxis()->GetBinLowEdge( ( m_histograms.at(0) )->GetNbinsX()+1 );
      r_hist = new TH1D( "r_hist", "real efficiency", m_nPtBins_Linear-1, rmin, rmax );
    }
    r_hist->SetCanExtend(TH1::kXaxis);

    r_hist->GetYaxis()->SetTitle("Real efficiency");
    r_hist->GetYaxis()->SetRangeUser(0.0,1.0);

    std::string xtitle("");
    if ( m_flavour == kFlavour::MUON ) { xtitle += "muon pT [GeV]"; }
    if ( m_flavour == kFlavour::ELEC ) { xtitle += "electron pT [GeV]"; }

    r_hist->GetXaxis()->SetTitle(xtitle.c_str());

    outtextfile << "Real efficiency - " << xtitle << "\n";
    for ( auto idx(0); idx < m_nPtBins_Linear; ++idx ) {
       if ( m_debug ) { std:: cout << "Bin idx " << idx+1 << " central value: " << ( m_histograms.at(0) )->GetXaxis()->GetBinCenter(idx + 1) << " - value to fill in: " << m_r_vals.at(idx) << std::endl; }
       r_hist->Fill( ( m_histograms.at(0) )->GetXaxis()->GetBinCenter(idx + 1), m_r_vals.at(idx) );
       r_hist->SetBinError( idx + 1, std::get<2>(m_r_errs.at(idx)) );
       outtextfile << "{ Bin nr: " << idx << ", efficiency = " <<  m_r_vals.at(idx) << " + " << std::get<0>(m_r_errs.at(idx)) << " - " << fabs( std::get<1>(m_r_errs.at(idx)) ) << " ( +- " << std::get<2>(m_r_errs.at(idx)) << " ) }\n";
    }

    r_hist->Write();
  }

  // --------------------
  // fake efficiency
  // --------------------

  if ( m_efficiency == kEfficiency::FAKE ) {

    TH1D *f_hist(nullptr);
    if ( m_doRebinning && m_useVariableBins ) {
	f_hist = new TH1D( "f_hist", "fake efficiency", m_newNBins, m_newBins );
    } else {
      double rmin = ( m_histograms.at(0) )->GetXaxis()->GetBinLowEdge(1);
      double rmax = ( m_histograms.at(0) )->GetXaxis()->GetBinLowEdge( ( m_histograms.at(0) )->GetNbinsX()+1 );
      f_hist = new TH1D( "f_hist", "fake efficiency", m_nPtBins_Linear-1, rmin, rmax );
    }
    f_hist->SetCanExtend(TH1::kXaxis);

    f_hist->GetYaxis()->SetTitle("Fake efficiency");
    f_hist->GetYaxis()->SetRangeUser(0.0,1.0);

    std::string xtitle("");
    if ( m_flavour == kFlavour::MUON ) { xtitle += "muon pT [GeV]"; }
    if ( m_flavour == kFlavour::ELEC ) { xtitle += "electron pT [GeV]"; }

    f_hist->GetXaxis()->SetTitle(xtitle.c_str());

    outtextfile << "Fake efficiency - " << xtitle << "\n";
    for ( auto idx(0); idx < m_nPtBins_Linear; ++idx ) {
       if ( m_debug ) { std:: cout << "Bin idx " << idx+1 << " central value: " << ( m_histograms.at(0) )->GetXaxis()->GetBinCenter(idx + 1) << " - value to fill in: " << m_f_vals.at(idx) << std::endl; }
       f_hist->Fill( ( m_histograms.at(0) )->GetXaxis()->GetBinCenter(idx + 1), m_f_vals.at(idx) );
       f_hist->SetBinError( idx + 1, std::get<2>(m_f_errs.at(idx)) );
       outtextfile << "{ Bin nr: " << idx << ", efficiency = " <<  m_f_vals.at(idx) << " + " << std::get<0>(m_f_errs.at(idx)) << " - " << fabs( std::get<1>(m_f_errs.at(idx)) ) << " ( +- " << std::get<2>(m_f_errs.at(idx)) << " ) }\n";
    }

    f_hist->Write();
  }

  outfile.Close();
  outtextfile.close();

}

// ----------------------------------------------------------------------------------------------------------------------

// ------------------------------------------------------
// Call this function from command line
// ------------------------------------------------------

int main( int argc, char **argv ) {

    std::cout << "Starting up..." << std::endl;

    TH1::SetDefaultSumw2(kTRUE);

    //gSystem->Load( "libCintex.so" );
    //gROOT->ProcessLine("Cintex::Cintex::Enable();");

    ///if ( argc<2 ) {
    //   std::cout << "Missing input parameters: " << std::endl;
    //    std::cout << "[1] input path" << std::endl;
    //    return 0;
    //}

    //const char* input_name = argv[1];
    //std::string input(input_name);

    // ----------------------------------------------------

    //const std::string tp_path("../OutputPlots_MMRates_25ns_v7_FinalSelection_LHComparison/Rates_NoSub_LHInput_6x6bins/");
    //const std::string input_path("../OutputPlots_MMRates_LHFit_2DPt/");

    const std::string tp_path("../OutputPlots_MMRates_25ns_v7_FinalSelection_NominalBinning/Rates_NoSub_LHInput/");
    const std::string input_path("../OutputPlots_MMRates_LHFit_25ns_v7_FinalSelection_NominalBinning/");

    // real efficiency - e

    LHFitter real_e( LHFitter::kFlavour::ELEC, LHFitter::kEfficiency::REAL );
    real_e.setVerbosity(LHFitter::kVerbosity::DEBUG);
    real_e.setTagAndProbePath(tp_path);
    real_e.setInputHistPath(input_path);
    real_e.m_doSubtraction = true;
    // REBINNING
    real_e.m_doRebinning = true;
    //real_e.setBinGrouping(2);
    double real_e_new_bins[8] = {10.0,15.0,20.0,25.0,30.0,40.0,60.0,200.0};
    real_e.setVariableBins( real_e_new_bins, 7 );
    real_e.initialise();
    real_e.fit();

    // real efficiency - mu

    LHFitter real_mu( LHFitter::kFlavour::MUON, LHFitter::kEfficiency::REAL );
    //real_mu.setVerbosity(LHFitter::kVerbosity::DEBUG);
    real_mu.setTagAndProbePath(tp_path);
    real_mu.setInputHistPath(input_path);
    real_mu.m_doSubtraction = true;
    // REBINNING
    real_mu.m_doRebinning = true;
    //real_mu.setBinGrouping(2);
    double real_mu_new_bins[8] = {10.0,15.0,20.0,25.0,30.0,40.0,60.0,200.0};
    real_mu.setVariableBins( real_mu_new_bins, 7 );
    real_mu.initialise();
    real_mu.fit();

    // fake efficiency - e
    ///*
    LHFitter fake_e( LHFitter::kFlavour::ELEC, LHFitter::kEfficiency::FAKE );
    fake_e.setVerbosity(LHFitter::kVerbosity::DEBUG);
    fake_e.setTagAndProbePath(tp_path);
    fake_e.setInputHistPath(input_path);
    fake_e.m_doSubtraction = true;
    // REBINNING
    fake_e.m_doRebinning = true;
    //fake_e.setBinGrouping(2);
    double fake_e_new_bins[6] = {10.0,15.0,20.0,25.0,40.0,200.0};
    fake_e.setVariableBins( fake_e_new_bins, 5 );
    fake_e.initialise();
    fake_e.fit();

    // fake efficiency - mu

    LHFitter fake_mu( LHFitter::kFlavour::MUON, LHFitter::kEfficiency::FAKE );
    fake_mu.setVerbosity(LHFitter::kVerbosity::DEBUG);
    fake_mu.setTagAndProbePath(tp_path);
    fake_mu.setInputHistPath(input_path);
    fake_mu.m_doSubtraction = true;
    // REBINNING
    fake_mu.m_doRebinning = true;
    fake_mu.m_doRebinning = true;
    //fake_mu.setBinGrouping(2);
    double fake_mu_new_bins[6] = {10.0,15.0,20.0,25.0,35.0,200.0};
    fake_mu.setVariableBins( fake_mu_new_bins, 5 );
    fake_mu.initialise();
    fake_mu.fit();

    //*/
    std::cout << "End of program!" << std::endl;
    return 0;

}
