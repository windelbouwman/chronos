#include "signalviewer.h"

SignalViewer::SignalViewer(QWidget *parent) : QWidget(parent)
{
  m_data[0] = 1;
  m_data[1] = 5;
  m_data[2] = 3;
  m_data[3] = 7;
  m_data[4] = 9;
  m_data[5] = 3;
  m_data[6] = 1;
  m_data[7] = 3;
  m_data[8] = 9;
  m_data[9] = 2;

  // Construct chart:
  m_chart = new QtCharts::QChart;

  m_series = new QtCharts::QLineSeries;
  m_chart->addSeries(m_series);

  QtCharts::QChartView *chartView = new QtCharts::QChartView(m_chart);
  // chartView->

  // Setup layout:
  QVBoxLayout *mainLayout = new QVBoxLayout;
  mainLayout->addWidget(chartView);
  setLayout(mainLayout);
}
