#ifndef SIGNALVIEWER_H
#define SIGNALVIEWER_H

#include <QWidget>
#include <QtCharts>


class SignalViewer : public QWidget
{
    Q_OBJECT
public:
    explicit SignalViewer(QWidget *parent = 0);

private:
    double m_data[10];
    QtCharts::QChart *m_chart;
    QtCharts::QLineSeries *m_series;

signals:

public slots:
};

#endif // SIGNALVIEWER_H
