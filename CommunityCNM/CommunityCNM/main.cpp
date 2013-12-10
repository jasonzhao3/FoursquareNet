//
//  main.cpp
//  CommunityCNM
//
//  Created by Jason Zhao on 12/10/13.
//  Copyright (c) 2013 Jason Zhao. All rights reserved.
//

#include <iostream>
#include "Snap.h"




int main(int argc,  char * argv[])
{
    
    //const => to unconst fail
    Env = TEnv(argc, argv, TNotify::StdNotify);
    Env.PrepArgs(TStr::Fmt("Network community detection. build: %s, %s. Time: %s", __TIME__, __DATE__, TExeTm::GetCurTm()));
    TExeTm ExeTm;
    Try
    const TStr InFNm = Env.GetIfArgPrefixStr("-i:", "/Users/jasonzhao/Documents/Courses/CS224W/Project/DataSet/GraphData/undirected_graph.txt", "Input graph (undirected graph)");
    const TStr OutFNm = Env.GetIfArgPrefixStr("-o:", "communities.txt", "Output file");
    const int CmtyAlg = Env.GetIfArgPrefixInt("-a:", 2, "Algorithm: 1:Girvan-Newman, 2:Clauset-Newman-Moore");
    const TStr WeightFile = Env.GetIfArgPrefixStr("-w:", "/Users/jasonzhao/Documents/Courses/CS224W/Project/DataSet/GraphData/node_weight.txt", "Node Weight File");
    
    //Load graph
    //    TFIn FIn(InFNm.CStr());
    //    PUNGraph Graph = TUNGraph::Load(FIn);
    PUNGraph Graph = TSnap::LoadEdgeList<PUNGraph>(InFNm);
    
    //Load WeightFile
    printf("come here\n");
    TSsParser Ss(WeightFile, ssfWhiteSep, true, true, true);
    THash<TInt, TInt> NodeWeight;
    int Nid, Weight;
    while (Ss.Next()) {
        if (! Ss.GetInt(0, Nid) || ! Ss.GetInt(1, Weight)) {continue;}
        NodeWeight.AddDat(Nid, Weight);
    }
    
    
    
    TSnap::DelSelfEdges(Graph);
    TCnComV CmtyV;
    double Q = 0.0;
    TStr CmtyAlgStr;
    if (CmtyAlg == 1) {
        CmtyAlgStr = "Girvan-Newman";
        Q = TSnap::CommunityGirvanNewman(Graph, CmtyV); }
    else if (CmtyAlg == 2) {
        CmtyAlgStr = "Cluset-Newman-Moore";
        std::cout<< "Ready to go!!" << std::endl;
        Q = TSnap::CommunityCNM(Graph, CmtyV, NodeWeight);
    }
    else { Fail; }
    
    
    FILE *F = fopen(OutFNm.CStr(), "wt");
    fprintf(F, "# Input: %s\n", InFNm.CStr());
    fprintf(F, "# Nodes: %d    Edges: %d\n", Graph->GetNodes(), Graph->GetEdges());
    fprintf(F, "# Algoritm: %s\n", CmtyAlgStr.CStr());
    fprintf(F, "# Modularity: %f\n", Q);
    fprintf(F, "# Communities: %d\n", CmtyV.Len());
    fprintf(F, "# NId\tCommunityId\n");
    for (int c = 0; c < CmtyV.Len(); c++) {
        for (int i = 0; i < CmtyV[c].Len(); i++) {
            fprintf(F, "%d\t%d\n", CmtyV[c][i].Val, c);
        }
    }
    fclose(F);
    
    Catch
    printf("\nrun time: %s (%s)\n", ExeTm.GetTmStr(), TSecTm::GetCurTm().GetTmStr().CStr());
    return 0;
    return 0;
}

