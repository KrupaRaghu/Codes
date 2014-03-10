#include "/home/janno/DREENE/lsvlm/src/util/util.h"
#include "/home/janno/DREENE/lsvlm/src/util/def.h"
#include "/home/janno/DREENE/lsvlm/src/language_models/lmfactory.h"
#include<string>

extern "C" {
    DynParams* new_DynParams(){
        return new DynParams();
    }

    void DynParams_SetParameter(DynParams* params, char* Identifier, float Value){
        return params->SetParameter(Identifier, Value);
    }

    void DynParams_SetParameterForLM(LM* lm, DynParams* params, char* paramName, float Value){
        return params->SetParameter(lm->GetName(), paramName, Value);
    }

    int DynParams_ExistsParameter(DynParams* params, char* LMName, char* parIdentifier){
        return params->ExistsParameter(LMName, parIdentifier);
    }

    float DynParams_RealParameter(DynParams* params, char* Identifier){
        return params->RealParameter(Identifier);
    }
    
    float DynParams_RealParameterForLM(DynParams* params, LM* lm, char* Identifier){
        return params->RealParameter(lm->GetName(), Identifier);
    }

    LMFactory* new_LMFactory(){
        return new LMFactory();
    }

    LM* LMFactory_StartLM(LMFactory* factory, char* lm_name, Vocabulary* V){
       return factory->StartLM(lm_name, V); 
    }

    Vocabulary* new_Vocabulary(char* filename){
        SectInStream *VocIn = new SectInStream(filename);
        VocIn->ScanSectHeader();
        Vocabulary* voc = new Vocabulary(VocIn);
        delete VocIn;
        return voc;
    }
    double LM_Prob(LM* lm, int *Hist, int M){
        return lm->Prob(Hist,M);
    }

    double LM_Score(LM* lm, int *Hist, int M){
        return lm->Score(Hist,M);
    }

    int LM_Update(LM* lm, int *Doc, int M, char* Key){
        return lm->Update(Doc, M, std::string(Key));
    }

    void LM_CollectParams(LM* lm, DynParams* params){
        return lm->CollectParams(params);
    }

    void LM_ReInit(LM* lm, DynParams* params){
        return lm->ReInit(params);
    }
}
