# asset_tree

The purpose of this project was to give a renewed view of the content of the paper [Dynamics of market correlations: Taxonomy and portfolio analysis](https://arxiv.org/abs/cond-mat/0302546), by using similar analysis throughout the last financial crisis. Data covers 2005-2012 and is based off EOD adjusted returns.

When implementing MST (minimum spanning tree), month to month average link length scales very similar with VIX.

![alt text](https://github.com/kark23/asset_tree/blob/master/link_l.png?raw=true)

From the same monthly trees, similar behavior to that shown in the paper is demonstrated for link survival ratio. Lower spikes in survival ratio mean the link structure of the asset tree are changing more quickly during this period of time. It makes sense that the lowest survival ratio is exhibited during the peak of the crisis, as this is a good example of market regime change. Note that values between the two analyses do not directly scale because if the different input space choice.

![alt text](https://github.com/kark23/asset_tree/blob/master/surv.png?raw=true)

The final result is to visualize the larger asset tree in a manner where conclusions can be made. Methodology here greatly diverges from that used in the paper. First MST is implemented in the same way as demonstrated earlier, but over the entire 7 year EOD adjusted return input space. Results from mst clustering were coming in somewhat odd, so K-Means clustering is applied to this same input space, with elbow method used to choose number of clusters (30 were used for the sake of granularity even though the elbow method may have suggested lower). The raw input space is then transformed to 2 dimensions using PCA in order to make it more visualizable. Finally, over this new input space the links/clusters are shown with ticker/industry information joined.

## Conclusion:
* MST average link length can be used as a decent proxy/alternative to VIX with this implementation
* Low link survival rate can be used as an indicator of market regime change and weakening of relationship stability between assets
* MST links and clustering can do a good job of differentiating industries, identifying closeness between industries, and linking potential candidates for pair/group trading
