from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('hello')

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .forms import CSVUploadForm


def analyze_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Read the uploaded CSV file using Pandas
            df = pd.read_csv(csv_file, encoding='unicode_escape')
            
            
            # Convert the 'Total Amount' column to numeric
            df['Total Amount'] = df['Total Amount'].str.replace(',', '').astype(float)
            # Convert the 'Posting Date' column to a datetime format
            df['Posting Date']= pd.to_datetime(df['Posting Date'])
            
            
            # filter dataframe between date
            filtered_df = df[(df['Posting Date'] >= pd.Timestamp(start_date)) & (df['Posting Date'] <= pd.Timestamp(end_date))]
            

            
            # Get the columns of the DataFrame
            columns = filtered_df.columns.tolist()
            
            
            # Perform your data analysis here, for example, displaying the first few rows
            preview_data = filtered_df.head(2)
            
            # Group by 'VendorName' and sum the 'Total Amount' for each vendor
            vendor_totals = filtered_df.groupby('VendorName')['Total Amount'].sum().reset_index()

            # Sort the vendors by 'Total Amount' in descending order and get the top 10
            top_10_vendors = vendor_totals.sort_values(by='Total Amount', ascending=False).head(10)
 
            # Create a Pie Chart using Plotly
            fig = px.pie(top_10_vendors, names='VendorName', values='Total Amount', title='Top 10 Vendors by Total Amount')
            fig.update_layout(width=1200, height=600) 

            # Convert the Plotly chart to HTML
            chart_div = fig.to_html(full_html=False)  
            
                     
            # Group by 'Item Description' and sum the 'Total Amount' for each item
            item_totals = filtered_df.groupby('Item Description')['Total Amount'].sum().reset_index()    
            # Sort the items by 'Total Amount' in descending order and get the top 10
            top_10_items = item_totals.sort_values(by='Total Amount', ascending=False).head(10)
            # Create a Bar Chart using Plotly
            figitem =go.Figure(data=[go.Bar(
                x=top_10_items['Item Description'],
                y=top_10_items['Total Amount'],
                text=top_10_items['Total Amount'],  # Display 'Total Amount' on top of bars
                textposition='auto',  # Automatically position the text on top of the bars
               
            )])
            figitem.update_layout(title='Top 10 Items by Total Amount')
            # Set the width and height of the Plotly figure to make it larger
            figitem.update_layout(width=1200, height=600) 
            # Convert the Plotly chart to HTML
            chart_item = figitem.to_html(full_html=False)      
            
                  
            # Convert 'Price' column to numeric
            filtered_df['Price'] = pd.to_numeric(filtered_df['Price'], errors='coerce')
            # Convert 'Quantity' column to numeric
            filtered_df['Quantity'] = pd.to_numeric(filtered_df['Quantity'], errors='coerce')           
            # Calculate the total Purchase             
            total_purchase  = (filtered_df['Price'] * filtered_df['Quantity']).sum()      
            # Group by month and sum the purchase amounts
            monthly_purchase = filtered_df.groupby(filtered_df['Posting Date'].dt.to_period("M"))['Total Amount'].sum().reset_index()  
            # Convert Period objects to string representations
            monthly_purchase['Posting Date'] = monthly_purchase['Posting Date'].dt.strftime('%Y-%m')             
            monthly_purchase_df = monthly_purchase.to_html(classes='table table-bordered  custom-table', index=False)             
                   
                   
            # Create a Line Chart for monthly purchase amounts
            fig_monthly = go.Figure(data=[go.Scatter(
                x=monthly_purchase['Posting Date'],
                y=monthly_purchase['Total Amount'],
                mode='lines+markers',  # Show lines and markers
            )])
            fig_monthly.update_layout(title='Monthly Purchase Amount')
            fig_monthly.update_layout(width=1200, height=600) 
            # Convert the Line chart to HTML
            chart_monthly = fig_monthly.to_html(full_html=False)
            
            
                                                                       
            context = {
                'form': form,
                'columns': columns,
                'preview_data': preview_data.to_html(classes='table table-bordered  custom-table', index=False),
                'top_10_vendors': top_10_vendors.to_html(classes='table table-bordered  custom-table', index=False),
                'chart_div': chart_div,
                'top_10_items':top_10_items.to_html(classes='table table-bordered  custom-table', index=False),
                'chart_item': chart_item,
                'total_purchase': total_purchase,  
                'monthly_purchase_df' :monthly_purchase_df,   
                'chart_monthly':chart_monthly,          

            }
            
            return render(request, 'topvendor.html', context)
    else:
        form = CSVUploadForm()

    return render(request, 'topvendor.html', {'form': form})