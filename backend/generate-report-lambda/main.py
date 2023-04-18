from src.report_generator import ReportGenerator


def lambda_handler(event, context):
    report_generator = ReportGenerator()
    report_generator.run(event)
    return True
