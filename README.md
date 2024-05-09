# <u>PROJECT</u>: CAR SERVICE **"AUTOMOTORS"**

    
![logo](https://user-images.githubusercontent.com/113382260/193469015-485cc23c-faef-4897-8617-2a5ee17470d7.png)
<br />
## Time Series - Data Science


### <i>Agustin F. Stigliano - Python Developer & Data Scientist</i>

<div>
    <p style="color:black;">Technical Presentation: <a href="https://chart-studio.plotly.com/~af.st22/61/b-style/#/">https://chart-studio.plotly.com/~af.st22/61/b-style/#/</a></p>
</div>

## <u>Project Description</u>
We are required to analyze the internal data of the company and make use of the "sells", "product_category", "location", and "employee" to figure out the impact of the pandemic on their business, and to present some solution that helps them make decisions. The data was treated both as a time series dataset and also as a discrete dataset, multiple interactive charts were presented in a web app slideshow presentation with the most relevant insights of each one of them.

The code presented in the **Technical Presentation** is a readable version that summarizes most of the work.<br />
The last lines of code are commented (at the bottom) because the output would break the current format.

After making EDA, and preprocessing, we use Plotly to create multiple plots at once, store them into an object, then execute sequentially all the charts, and select dynamically which one of them to save. After selecting the relevant charts, we uploaded them into **Chart-Studio** and obtained an embed iframe URL to use in our Jupyter Notebook directly on the web app slideshow (Mercury Framework).

The most relevant part done was to convert **from COP to USD** from the **Alpha Vantage API** in a weekly quotation.
