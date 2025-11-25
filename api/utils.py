import pandas as pd
import re

def get_analysis(query):
    try:
        df = pd.read_excel('Sample_data.xlsx')

        if 'final location' not in df.columns:
            return f"Column 'final location' not found. Available columns: {df.columns.tolist()}", [], []

      
        locations = re.findall(r'(Wakad|Akurdi|Aundh|Ambegaon Budruk)', query, flags=re.I)

       
        if len(locations) == 2 and "compare" in query.lower():
            loc1, loc2 = locations

            data1 = df[df['final location'].str.contains(loc1, case=False, na=False)]
            data2 = df[df['final location'].str.contains(loc2, case=False, na=False)]

            if data1.empty or data2.empty:
                return f"❌ Data not found for one or both locations.", [], []

            summary = (
                f"📊 **Comparison between {loc1} & {loc2}**\n"
                f"• {loc1}: Avg Sales ₹{data1['total_sales - igr'].mean():,.2f}\n"
                f"• {loc2}: Avg Sales ₹{data2['total_sales - igr'].mean():,.2f}\n"
                f"• 📈 Demand trends shown in comparison chart"
            )

            chart_data = [
                {
                    "location": loc1,
                    "data": data1.groupby('year')['total sold - igr'].mean().reset_index().to_dict('records')
                },
                {
                    "location": loc2,
                    "data": data2.groupby('year')['total sold - igr'].mean().reset_index().to_dict('records')
                }
            ]

            return summary, chart_data, []

       
        if "last 3 years" in query.lower():
            loc = locations[0] if locations else None
            if not loc:
                return "❌ Please specify a valid location.", [], []

            filtered = df[df['final location'].str.contains(loc, case=False, na=False)]
            max_year = filtered['year'].max()
            filtered = filtered[filtered['year'] >= max_year - 2]  

            if filtered.empty:
                return f"❌ Not enough recent data for {loc}.", [], []

            avg_sales = filtered['total_sales - igr'].mean()
            chart_data = filtered.groupby('year')['total_sales - igr'].mean().reset_index()

            summary = (
                f"📈 3-Year Sales Trend for **{loc}\n"
                f" 📊 Avg Sales: ₹{avg_sales:,.2f}\n"
                f"🔎 Recent years analyzed in chart"
            )

            return summary, chart_data.to_dict('records'), filtered.to_dict('records')

        
        area_name = query.strip()
        filtered = df[df['final location'].str.contains(area_name, case=False, na=False)]

        if filtered.empty:
            return f"❌ No data found for '{area_name}'. Try Wakad, Aundh, Akurdi, etc.", [], []

        avg_sales = filtered['total_sales - igr'].mean()
        chart_data = filtered.groupby('year')['total sold - igr'].mean().reset_index()

        # Trend calculation
        sorted_data = chart_data.sort_values('year', ascending=False)
        trend = "📈 rising (increasing demand)" if len(sorted_data) > 1 and sorted_data.iloc[0]['total sold - igr'] > sorted_data.iloc[1]['total sold - igr'] else "📉 declining"

        advice = "👍 Good for investment" if "rising" in trend else "⚠️ Consider carefully before investing"

        peak_year = int(chart_data.loc[chart_data['total sold - igr'].idxmax()]['year'])

        summary = (
            f"📍 Analysis for {area_name}\n"
            f"📊 Average yearly sales: ₹{avg_sales:,.2f}\n"
            f"🔥 Peak demand in: {peak_year}\n"
            f"📉 Current market trend: {trend}\n"
            f"🧠 Recommendation: {advice}"
        )

        return summary, chart_data.to_dict('records'), filtered.to_dict('records')

    except Exception as e:
        return f"⚠️ Error processing data: {e}", [], []
