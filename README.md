# asset_tree

The purpose of this project was to give a renewed view of the content of the paper [Dynamics of market correlations: Taxonomy and portfolio analysis (2003)](https://arxiv.org/abs/cond-mat/0302546), by using similar analysis throughout the last financial crisis. Data covers 2005-2012 and is based off EOD adjusted returns.

When implementing MST (minimum spanning tree), month to month average link length scales very similar with VIX. This intuitively makes sense as greater volatility would increase the distance metric within the return input space.

<div align="center">
  
![alt text](https://github.com/kark23/asset_tree/blob/master/figs/link_l.png?raw=true)
Figure 1: Experimental Average Link Length
![alt text](https://github.com/kark23/asset_tree/blob/master/figs/vix.PNG?raw=true)
Figure 2: VIX from FRED

</div>

From the same monthly trees, similar behavior to that shown in the paper is demonstrated for link survival ratio. Lower spikes in survival ratio mean the link structure of the asset tree are changing more quickly during this period of time. It makes sense that the lowest survival ratio is exhibited during the peak of the crisis, as this is a good example of market regime change. Note that values between the two analyses do not directly scale because if the different input space choice.

<div align="center">
  
![alt text](https://github.com/kark23/asset_tree/blob/master/figs/surv.png?raw=true)
Figure 3: Experimental Survival Ratio

![alt text](https://github.com/kark23/asset_tree/blob/master/figs/surv_ratio.PNG?raw=true)

Figure 4: Survival Ratio from: [Dynamics of market correlations: Taxonomy and portfolio analysis (2003)](https://arxiv.org/abs/cond-mat/0302546)

</div>

The final result is to visualize the larger asset tree in a manner where conclusions can be made. Methodology here greatly diverges from that used in the paper. First MST is implemented in the same way as demonstrated earlier, but over the entire 7 year EOD adjusted return input space. Results from mst clustering were coming in somewhat odd, so K-Means clustering is applied to this same input space, with elbow method used to choose number of clusters (30 were used for the sake of granularity even though the elbow method may have suggested lower). The raw input space is then transformed to 2 dimensions using PCA in order to make it more visualizable. Finally, over this new input space the links/clusters are shown with ticker/industry information joined.

<div align="center">

![alt text](https://github.com/kark23/asset_tree/blob/master/figs/elbow.png?raw=true)

Figure 5: Elbow method for K-Means clustering

![alt text](https://github.com/kark23/asset_tree/blob/master/figs/topology_tree.PNG?raw=true)

Figure 6: Asset Tree from: [Dynamics of market correlations: Taxonomy and portfolio analysis (2003)](https://arxiv.org/abs/cond-mat/0302546)

![alt text](https://github.com/kark23/asset_tree/blob/master/figs/full_tree1.png?raw=true)
Figure 7: Experimental Asset Tree (please click to view full)

</div>

## Conclusion:
* MST average link length can be used as a decent proxy/alternative to VIX with this implementation
* Low link survival rate can be used as an indicator of market regime change and weakening of relationship stability between assets
* MST links and clustering can differentiate industries, identify closeness between industries, and link potential candidates for pair/group trading
