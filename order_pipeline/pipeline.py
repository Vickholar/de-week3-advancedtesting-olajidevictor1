from .reader import Reader
from .validator import Validator
from .transformer import Transformer
from .analyzer import Analyzer
from .exporter import Exporter


class Pipeline:
    """Main pipeline orchestrator."""
    
    def __init__(self, input_path: str, output_path: str):
        """
        Initialize pipeline.
        
        Args:
            input_path: Path to input JSON file
            output_path: Path for output JSON file
        """
        self.reader = Reader(input_path)
        self.validator = Validator()
        self.transformer = Transformer()
        self.analyzer = Analyzer()
        self.exporter = Exporter(output_path)
    
    def run(self) -> dict:
        """
        Run the complete pipeline.
        
        Returns:
            Dictionary with pipeline results and statistics
        """
        # Read data
        print("Reading data...")
        raw_data = self.reader.read()
        print(f"Read {len(raw_data)} orders")
        
        # Validate
        print("\nValidating data...")
        valid_data = self.validator.validate(raw_data)
        validation_summary = self.validator.get_summary()
        print(f"Valid orders: {validation_summary['valid_rows']}")
        print(f"Invalid orders: {validation_summary['invalid_rows']}")
        
        if validation_summary['invalid_rows'] > 0:
            print("\nInvalid order reasons:")
            for reason, count in validation_summary['reasons'].items():
                print(f"  - {reason}: {count}")
        
        # Transform
        print("\nTransforming data...")
        transformed_data = self.transformer.transform(valid_data)
        print(f"Transformed {len(transformed_data)} orders")
        
        # Analyze
        print("\nAnalyzing data...")
        stats = self.analyzer.analyze(transformed_data)
        print(f"Total revenue: ${stats['total_revenue']:.2f}")
        print(f"Average revenue: ${stats['average_revenue']:.2f}")
        print(f"Payment status breakdown:")
        print(f"  - Paid: {stats['payment_status_counts']['paid']}")
        print(f"  - Pending: {stats['payment_status_counts']['pending']}")
        print(f"  - Refunded: {stats['payment_status_counts']['refunded']}")
        
        # Export
        print("\nExporting results...")
        self.exporter.export(transformed_data, stats)
        print(f"Results exported successfully")
        
        return {
            'validation_summary': validation_summary,
            'statistics': stats,
            'total_processed': len(transformed_data)
        }


if __name__ == '__main__':
    pipeline = Pipeline('shoplink.json', 'shoplink_cleaned.json')
    results = pipeline.run()
    print("\n" + "="*50)
    print("Pipeline completed successfully!")
    print(f"Processed {results['total_processed']} orders")
    print("="*50)