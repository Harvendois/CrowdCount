# Crowd Count by Cho
Hi, this is a documentation of my use of the Crowd Counting Computer Vision project, provided by @Leeyeehoo and directed by AnalyticsVidhya's article. 
This documentation is useful for following reasons: 
1. It has already corrected @Leeyeehoo's project according to AnalyticsVidhya's article and also where AnalyticsVidhya missed. 
2. It is corrected based on the Shanghaitech Dataset that you can get from Kaggle, which is slightly different from that used by AnalyticsVidhya's article nor @Leeyeehoo. 
3. You can easily change your root directory and .json files by using the converter.py that I provided. 
-------------------------
## Information: 
+ I am using a laptop with RTX3050, and it took my laptop about 40 hours to train 360~epochs.
+ The MAE after validation gave me about 69 MAE, better than 75 MAE given by AnalyticsVidhya. 
+ After about 280ish epochs, the loss barely decreases. Sharp reduction of loss was seen after 30-50 epochs. 
+ I think the loss was within 30 people (even with the outliers) when it reached 150 epochs. That could be good enough. 
+ After 360 epochs, the loss is within 1 digit, but sometimes outliers could reach about 15 people. 
-------------------------

![alt text](https://github.com/[Harvendois]/[CrowdCount]/blob/[main]/actual_try_with_a_different_pci.png?raw=true)
