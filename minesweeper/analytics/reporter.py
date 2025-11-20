import os
import tempfile
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import matplotlib.pyplot as plt
import numpy as np


class PDFReporter:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        # Create custom styles for better formatting
        self.styles.add(ParagraphStyle(
            name='AnalyticsTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='Statistics',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=colors.darkgreen
        ))
    
    def generate_analytics_report(self, analytics_data, config, sample_size, output_path=None):
        """
        Generate a comprehensive PDF report for analytics results
        """
        # Use provided path or generate default in analytics_reports folder
        if output_path is None:
            output_path = self._get_default_output_path(config)
        
        print(f"Generating PDF report at: {output_path}")  # Debug info
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # Cover Page
        story.extend(self._create_cover_page(config, sample_size))
        story.append(PageBreak())
        
        # Summary Page
        story.extend(self._create_summary_page(analytics_data, config, sample_size))
        story.append(PageBreak())
        
        # Detailed Analytics
        story.extend(self._create_detailed_analytics(analytics_data, config))
        
        doc.build(story)
        return output_path
    
    def _create_cover_page(self, config, sample_size):
        """Create the cover page with title and configuration info"""
        rows, cols, mines = config
        
        elements = []
        
        # Title
        title_style = ParagraphStyle(
            name='CoverTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=24,
            textColor=colors.darkblue,
            alignment=1  # Center aligned
        )
        
        elements.append(Paragraph("MINESWEEPER ANALYTICS REPORT", title_style))
        elements.append(Spacer(1, 0.5*inch))
        
        # Configuration Info
        config_text = f"""
        <b>Board Configuration:</b><br/>
        • Size: {rows} × {cols} cells<br/>
        • Mines: {mines}<br/>
        • Sample Size: {sample_size} boards<br/>
        • Mine Density: {(mines/(rows*cols))*100:.1f}%<br/>
        """
        
        elements.append(Paragraph(config_text, self.styles['Normal']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Generation info
        date_info = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        elements.append(Paragraph(date_info, self.styles['Italic']))
        
        return elements
    
    def _create_summary_page(self, analytics_data, config, sample_size):
        """Create summary page with key statistics"""
        rows, cols, mines = config
        
        elements = []
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.styles['Heading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Key Statistics Table
        stats_data = [
            ['Metric', 'Value', 'Description'],
            ['Board Size', f'{rows} × {cols}', 'Rows × Columns'],
            ['Total Mines', str(mines), 'Number of mines placed'],
            ['Sample Size', str(sample_size), 'Boards analyzed'],
            ['Mine Density', f'{(mines/(rows*cols))*100:.1f}%', 'Percentage of mines'],
            ['Avg White Cells', f'{np.mean(analytics_data["white_counts"]):.1f}', 'Average blank cells per board'],
            ['Avg Mine Clusters', f'{np.mean(analytics_data["cluster_counts"]):.1f}', 'Average clusters per board'],
            ['Most Common Number', f'{np.argmax(analytics_data["number_freq"])}', 'Most frequent cell value']
        ]
        
        stats_table = Table(stats_data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(stats_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Additional insights
        insights = self._generate_insights(analytics_data, config)
        elements.append(Paragraph("Key Insights:", self.styles['Heading2']))
        for insight in insights:
            elements.append(Paragraph(f"• {insight}", self.styles['Normal']))
        
        return elements
    
    def _create_detailed_analytics(self, analytics_data, config):
        """Create detailed analytics pages with plots - FIXED PAGE BREAKS"""
        elements = []
        
        elements.append(Paragraph("DETAILED ANALYTICS", self.styles['Heading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        # White Cells Distribution
        elements.append(Paragraph("White Cells Distribution", self.styles['AnalyticsTitle']))
        white_plot_path = self._create_white_cells_plot(analytics_data['white_counts'])
        elements.extend(self._create_image_with_caption(white_plot_path, 
                    "Distribution of white (blank) cells across analyzed boards"))
        elements.append(Spacer(1, 0.2*inch))
        
        # Number Frequency Distribution
        elements.append(Paragraph("Cell Value Distribution", self.styles['AnalyticsTitle']))
        number_plot_path = self._create_number_frequency_plot(analytics_data['number_freq'])
        elements.extend(self._create_image_with_caption(number_plot_path,
                    "Frequency of different cell values (0-8 mines in neighborhood)"))
        elements.append(Spacer(1, 0.2*inch))
        
        # CHANGED: Add page break BEFORE Mine Cluster Analysis
        elements.append(PageBreak())
        
        # Mine Clusters - NOW ON PAGE 4
        elements.append(Paragraph("Mine Cluster Analysis", self.styles['AnalyticsTitle']))
        cluster_plot_path = self._create_cluster_plot(analytics_data['cluster_counts'])
        elements.extend(self._create_image_with_caption(cluster_plot_path,
                    "Distribution of mine clusters per board"))
        elements.append(Spacer(1, 0.2*inch))
        
        # Heatmap
        elements.append(Paragraph("Mine Neighborhood Heatmap", self.styles['AnalyticsTitle']))
        heatmap_plot_path = self._create_heatmap_plot(analytics_data['heatmap'], config)
        elements.extend(self._create_image_with_caption(heatmap_plot_path,
                    "Average number of mines in 3×3 neighborhood around each cell"))
        
        return elements
    
    def _create_white_cells_plot(self, white_counts):
        """Create white cells histogram plot - IMPROVED VERSION"""
        fig, ax = plt.subplots(figsize=(10, 5))  # CHANGED: Larger size
        ax.hist(white_counts, bins=20, color='skyblue', edgecolor='black', alpha=0.7)  # CHANGED: More bins
        ax.set_xlabel('Number of White Cells', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title('Distribution of White Cells per Board', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add statistics with better positioning
        mean_val = np.mean(white_counts)
        std_val = np.std(white_counts)
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.1f}')
        ax.legend(fontsize=10)
        
        # CHANGED: Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        temp_path = self._save_temp_plot(fig, "white_cells")
        return temp_path
    
    def _create_number_frequency_plot(self, number_freq):
        """Create number frequency bar chart - IMPROVED VERSION"""
        fig, ax = plt.subplots(figsize=(10, 5))  # CHANGED: Larger size
        values = range(9)
        colors_plot = ['lightblue', 'blue', 'green', 'red', 'purple', 
                    'orange', 'brown', 'pink', 'gray']
        
        bars = ax.bar(values, number_freq, color=colors_plot, edgecolor='black', alpha=0.7)
        ax.set_xlabel('Cell Value (Number of Adjacent Mines)', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title('Distribution of Cell Values', fontsize=14, fontweight='bold')
        ax.set_xticks(values)
        
        # CHANGED: Improve value labels for large numbers
        for bar, freq in zip(bars, number_freq):
            height = bar.get_height()
            if height > 0:
                # Format large numbers with commas
                formatted_freq = f'{int(freq):,}' if freq >= 1000 else f'{int(freq)}'
                ax.text(bar.get_x() + bar.get_width()/2., height,
                    formatted_freq, ha='center', va='bottom', fontsize=9)
        
        # CHANGED: Rotate x-axis labels if needed for large boards
        if max(number_freq) > 10000:
            plt.xticks(rotation=45)
        
        plt.tight_layout()
        temp_path = self._save_temp_plot(fig, "number_freq")
        return temp_path
    
    def _create_cluster_plot(self, cluster_counts):
        """Create mine clusters histogram - IMPROVED VERSION"""
        fig, ax = plt.subplots(figsize=(10, 5))  # CHANGED: Larger size
        
        if cluster_counts:
            # CHANGED: Better bin calculation for large ranges
            data_range = max(cluster_counts) - min(cluster_counts)
            bins = min(20, data_range + 1)  # Limit bins to prevent overcrowding
            
            ax.hist(cluster_counts, bins=bins, color='lightcoral', 
                edgecolor='black', alpha=0.7)
            ax.set_xlabel('Number of Mine Clusters', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.set_title('Distribution of Mine Clusters per Board', fontsize=14, fontweight='bold')
            
            # CHANGED: Better x-axis ticks for large ranges
            if data_range > 20:
                step = max(1, data_range // 10)
                ax.set_xticks(range(min(cluster_counts), max(cluster_counts) + 1, step))
        
        plt.tight_layout()
        temp_path = self._save_temp_plot(fig, "clusters")
        return temp_path
    
    def _create_heatmap_plot(self, heatmap, config):
        """Create heatmap visualization - IMPROVED VERSION"""
        rows, cols, _ = config
        fig, ax = plt.subplots(figsize=(12, 8))  # CHANGED: Larger size for big boards
        
        im = ax.imshow(heatmap, cmap='YlOrRd', aspect='auto')
        ax.set_xlabel('Column', fontsize=12)
        ax.set_ylabel('Row', fontsize=12)
        ax.set_title('Average Mines in 3×3 Neighborhood', fontsize=14, fontweight='bold')
        
        # CHANGED: Adjust ticks for large boards
        if cols > 20:
            x_ticks = range(0, cols, max(1, cols // 10))
            ax.set_xticks(x_ticks)
        if rows > 20:
            y_ticks = range(0, rows, max(1, rows // 10))
            ax.set_yticks(y_ticks)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Average Mine Count', fontsize=10)
        
        # Add grid (lighter for large boards)
        grid_alpha = 0.1 if max(rows, cols) > 20 else 0.3
        ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
        ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.2, alpha=grid_alpha)
        ax.tick_params(which="minor", size=0)
        
        plt.tight_layout()
        temp_path = self._save_temp_plot(fig, "heatmap")
        return temp_path
    
    def _create_image_with_caption(self, image_path, caption):
        """Create an image with caption in PDF - FIXED VERSION"""
        elements = []
        img = Image(image_path, width=6*inch, height=3*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph(f"<i>{caption}</i>", self.styles['Italic']))
        return elements
    
    def _save_temp_plot(self, fig, prefix):
        """Save plot to temporary file and return path"""
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"{prefix}_{datetime.now().strftime('%H%M%S')}.png")
        fig.savefig(temp_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return temp_path
    
    def _generate_insights(self, analytics_data, config):
        """Generate analytical insights from the data"""
        rows, cols, mines = config
        insights = []
        
        white_mean = np.mean(analytics_data['white_counts'])
        cluster_mean = np.mean(analytics_data['cluster_counts'])
        mine_density = mines / (rows * cols)
        
        insights.append(f"Average of {white_mean:.1f} white cells per board ({white_mean/(rows*cols)*100:.1f}% of board)")
        
        if mine_density > 0.2:
            insights.append("High mine density suggests challenging gameplay")
        else:
            insights.append("Moderate mine density allows for strategic play")
        
        if cluster_mean < mines * 0.1:
            insights.append("Mines tend to form few large clusters")
        else:
            insights.append("Mines are distributed across multiple clusters")
        
        most_common_num = np.argmax(analytics_data['number_freq'])
        insights.append(f"Most common cell value is {most_common_num} adjacent mines")
        
        return insights
    
    def _get_default_output_path(self, config):
        """Get output path in game's analytics_reports folder"""
        rows, cols, mines = config
        
        # Create analytics_reports folder in current directory
        analytics_dir = "analytics_reports"
        os.makedirs(analytics_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"minesweeper_analytics_{rows}x{cols}_{mines}mines_{timestamp}.pdf"
        
        return os.path.join(analytics_dir, filename)