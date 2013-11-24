#! /usr/bin/env/python 3.1
#
# Class which handles the creation of an html-report
# author: Andreas Wagner
#
import time
class HTMLReport(object):
    
      def __init__(self, mainResult, scannerResultMap, securityModelResultMap, outputFilePath):
          self.scannerResultMap = scannerResultMap
          self.securityModelResultMap = securityModelResultMap
          self.outputFilePath = outputFilePath
          self.mainResult = mainResult
          
          
      def buildHTMLHead(self, file):
          file.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">')
          file.write("<html>")
          file.write("<head>")
          file.write('<meta http-equiv="Content-type" content="text/html;charset=UTF-8">')
          file.write('<meta name="author" content="Ing. Andreas Wagner, BSc">')
          file.write("<title>AnalyzeTool-Report</title>")
          file.write('<link rel="stylesheet" type="text/css" href="reportStyle.css">')
          file.write('<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>')
          file.write('<script text="text/javascript" src="http://code.highcharts.com/highcharts.js"> </script>')
          file.write('<script type="text/javascript">jQuery.noConflict();</script>')
          file.write("</head>")
          
          
      def buildBody(self, file):
          
          issueOverviewTable = '<table class="defaultTable"><tr><td>Scanner</td><td>Real Issues</td><td>Other Issues</td></tr>'
          issueOverviewTable+='<tr><td>Juliet</td><td>'+str(self.mainResult.issueCnt)+'</td><td>0</td></tr>'
          categories = "categories: ['Total Issues'"
          
          realIssues="{name: 'Real Issues', data: ["+str(self.mainResult.issueCnt)
          foundIssues="{name: 'other found issues', data: [0"
          for key, value in self.scannerResultMap.items():   
              if(key!='JULIET'):           
                  categories+=", '"+key+"'"
                  #series+="}, {name: "+"'"+key+"', data: ["+str(value.realIssues)+", "+str(value.issueCnt)+"]"
                  realIssues+=", "+str(value.realIssues)
                  foundIssues+=", "+str(value.issueCnt-value.realIssues)
                  issueOverviewTable+='<tr><td>'+key+'</td><td>'+str(value.realIssues)+'</td><td>'+str(value.issueCnt-value.realIssues)+'</td></tr>'
              
          realIssues+="]}"
          foundIssues+="]}"
          categories+="]"
          issueOverviewTable+='</table>'
          series = "series: ["+realIssues+", "+foundIssues+"]"
          file.write('<body>')
          file.write("<center><h1>Security-Scanner Report <br/>"+time.strftime("%Y-%m-%d")+"</h1></center>")
          file.write('<div id="summaryDiv" class="detailMain">')
          file.write("<h3>Overview</h3>")
          file.write('<div id="summaryChart"></div>')
          file.write('''<script type="text/javascript">

(function($){ // encapsulate jQuery

$(function () {
        $('#summaryChart').highcharts({
            chart: {
                type: 'column'
            },
            title: {
                text: 'Report-Overview',
                style : {
                        fontSize : '20px'
                    }
            },
            xAxis: {''')
          file.write(categories)
          
          #      categories: ['Total Issues', 'Oranges', 'Pears', 'Grapes', 'Bananas']
          file.write('''
            ,labels : {
                style : {
                    fontSize : '18px'
                }
            } 
            },
            yAxis: {
                min: 0,
                stackLabels: {
                    enabled: true,
                    style: {
                        fontWeight: 'bold',
                        color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray',
                        fontSize : '18px'
                    }
                }
                 ,labels : {
                style : {
                    fontSize : '18px'
                }
            } 
            },
            legend: {
                align: 'right',
                x: -100,
                verticalAlign: 'top',
                y: 20,
                floating: true,
                backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColorSolid) || 'white',
                borderColor: '#CCC',
                borderWidth: 1,
                shadow: false,
                itemStyle : {
                    fontSize : '18px'
                }
            },
            tooltip: {
                formatter: function() {
                    return '<b>'+ this.x +'</b><br/>'+
                        this.series.name +': '+ this.y +'<br/>'+
                        'Total: '+ this.point.stackTotal;
                }
            },
            plotOptions: {
                column: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: true,
                        color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
                        style : {
                            fontSize : '18px'
                        }
                    }
                }
            },''')
          file.write(series)
          file.write('''
            
        });
    });
    

})(jQuery);
</script>''')
          file.write(issueOverviewTable)
          file.write("<br/>")
          self.buildSecurityModelOverview(file)
          file.write("</div>")
          #file.write("<h2>DetailData</h2>")
          
          for key, value in self.scannerResultMap.items():
              file.write('<div id="'+key.lower()+'_main" class="detailMain">')
              file.write('<h3>'+key.upper()+"</h3>")
              file.write('<div id="'+key.lower()+'_content">')
              containerId = "pie_"+key
              #pieTable = '<table><tr><th>correct line matches</th><th>different line matches</th><th>range matches</th><th>different type matches</th><th>none matching</th></tr>'
              pieTable='<div id="'+key+'_pietable"><table class="defaultTable pietable"><tr><td>Type</td><td>Number</td></tr>'
              data='data:['
              data+="['correct line matches',"+str(value.correctMatchCnt)+"],"
              pieTable+="<tr><td>correct line matches</td><td>"+str(value.correctMatchCnt)+"</td></tr>"
              data+="['different line matches',"+str(str(value.differentLineMatches))+"],"
              pieTable+="<tr><td>different line matches</td><td>"+str(value.differentLineMatches)+"</td></tr>"
              data+="['range matches',"+str(value.rangeMatch)+"],"
              pieTable+="<tr><td>range matches</td><td>"+str(value.rangeMatch)+"</td></tr>"
              data+="['different type matches',"+str(value.differentTypeMatches)+"],"
              pieTable+="<tr><td>different type matches</td><td>"+str(value.differentTypeMatches)+"</td></tr>"
              data+="['none matching',"+str(value.noneMatching)+"]]"
              pieTable+="<tr><td>none matching</td><td>"+str(value.noneMatching)+"</td></tr></table></div>"
             # pieTable+='<tr><td>'+str(value.correctMatchCnt)+'</td><td>'+str(value.differentLineMatches)+'</td><td>'+str(value.rangeMatch)+'</td><td>'+str(value.differentTypeMatches)+'</td><td>'+str(value.noneMatching)+'</td></tr></table>'
              
              file.write('<div id="'+containerId+'" class="pieChart"></div>')
              file.write('''<script type="text/javascript">(function($){ // encapsulate jQuery
          
          $(function () {''')
              file.write(" $('#"+containerId+"').highcharts({")
              file.write('''
   
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: 'Issue distribution',
            style : {
                        fontSize : '20px'
                    }
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    color: '#000000',
                    connectorColor: '#000000',
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style : {
                        fontSize : '18px'
                    }
                }
            }
        },
        series: [{
            type: 'pie',
            name: 'Issue Distribution',
           ''')
              file.write(data)
              file.write('''
        }]
    });
});})(jQuery);</script>''')
              
              file.write(pieTable)
              file.write('<div style="clear:both"></div>')
              file.write("<br/>")
              self.buildSecurityModelDetailData(key, file)
              file.write('</div>')
              file.write('</div>')
          file.write('<div id="summaryIssueDistribution" class="detailMain">')
          file.write("<h3>Summary Issue distribution</h3>")
          self.buildOverallSummary(file);
          file.write('</div>')
          
          self.printLegend(file)
          file.write('</body>')
    
    
      def buildSecurityModelDetailData(self, scannerName, file):
          secIssues = self.securityModelResultMap[scannerName]
          
          
          
          compareResultMap = secIssues.compare()
          containerId="secmodel_"+scannerName
          categories = "categories: ["
          corrLineMatch="{name: 'correct line matches', data: ["
          diffLineMath="{name: 'different line matches', data: ["
          rangeMatch="{name: 'range matches', data: ["
          diffTypeMatch="{name: 'different type matches', data: ["
          noneMatch="{name: 'none matching', data: ["
          
          detailTable='<table class="defaultTable"><tr><td>Class</td><td>correct line matches</td><td>different line matches</td><td>range matches</td><td>different type matches</td><td>none matching</td></tr>'
          firstRun = True
          for weaknessClass, resultHolder in compareResultMap.items():
              
              
              if(not firstRun):
                 
                  corrLineMatch+=", "
                  diffLineMath+=", "
                  rangeMatch+=", "
                  diffTypeMatch+=", "
                  noneMatch+=", "
                  categories+=", "
              firstRun = False
              categories+="'"+weaknessClass+"'"
              
              corrLineMatch+=str(resultHolder.correctMatchCnt)
              diffLineMath+=str(resultHolder.differentLineMatches)
              rangeMatch+=str(resultHolder.rangeMatch)
              diffTypeMatch+=str(resultHolder.differentTypeMatches)
              noneMatch+=str(resultHolder.noneMatching)
              detailTable+='<tr><td>'+weaknessClass+'</td><td>'+str(resultHolder.correctMatchCnt)+'</td><td>'+str(resultHolder.differentLineMatches)+'</td><td>'+str(resultHolder.rangeMatch)+'</td><td>'+str(resultHolder.differentTypeMatches)+'</td><td>'+str(resultHolder.noneMatching)+'</td></tr>'
              
          corrLineMatch+="]}"
          diffLineMath+="]}"
          rangeMatch+="]}"
          diffTypeMatch+="]}"
          noneMatch+="]}"
          categories+="]"
          detailTable+='</table>'
          series = "series: ["+corrLineMatch+", "+diffLineMath+", "+rangeMatch+", "+diffTypeMatch+", "+noneMatch+"]"
                            
          file.write('<div id="'+containerId+'"></div>')
          file.write('''<script type="text/javascript">

(function($){ // encapsulate jQuery

$(function () {''')
          file.write("$('#"+containerId+"').highcharts({")
          file.write('''
            chart: {
                type: 'bar'
            },
            title: {
                text: 'Security-Model',
                style : {
                        fontSize : '20px'
                    }
            },
            xAxis: {''')
          file.write(categories)
          
          #      categories: ['Total Issues', 'Oranges', 'Pears', 'Grapes', 'Bananas']
          file.write('''
            ,labels : {
                    style : {
                        fontSize : '18px'
                    }
            }},
            yAxis: {
                min: 0,
                labels : {
                    style : {
                        fontSize : '18px'
                    }
                }
            },
            legend: {
               
                backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColorSolid) || 'white',
                borderColor: '#CCC',
                borderWidth: 1,
                shadow: false,
                itemStyle : {
                        fontSize : '18px'
                    }
            },
            tooltip: {
                formatter: function() {
                    return '<b>'+ this.x +'</b><br/>'+
                        this.series.name +': '+ this.y +'<br/>'+
                        'Total: '+ this.point.stackTotal;
                }
            },
            plotOptions: {
                series: {
                    stacking: 'normal',
                    
                    pointPadding : 0.1,
                    groupPadding : 0.1
                }
            
            
            },''')
          file.write(series)
          file.write('''
            
        });
    });
    

})(jQuery);
</script>''')
          file.write(detailTable)
          
          
      def buildSecurityModelOverview(self, file):
          
          addCategories = True
          categories = "categories: ["
          seriesElem = "series: ["          
          tableBody=''
          tableHead='<tr><td>Scanner</td>'
          for scannerName, secIssues in self.securityModelResultMap.items():
              compareResultMap = secIssues.compare()            
              
              series="{name: '"+scannerName+"', stack:'"+scannerName+"', data: ["
          
              firstRun = True
              tableRow = '<tr><td>'+scannerName+'</td>'
              for weaknessClass, resultHolder in compareResultMap.items():
                  
                  
                  if(not firstRun):
                      series+=", "
                      if(addCategories):
                          categories+=", "
                  firstRun = False
                  
                  if(addCategories):
                      categories+="'"+weaknessClass+"'"
                      tableHead+='<td>'+weaknessClass+'</td>'
                  
                  
                  series+=str(resultHolder.realIssues)
                  tableRow+='<td>'+str(resultHolder.realIssues)+'</td>'
              
              series+="]}"
              tableRow+='</tr>'
              tableBody+=tableRow
              addCategories=False
              seriesElem+= series+", "
          seriesElem+="]"
          categories+="]"
          tableHead+='</tr>'
          htmlTable='<table class="defaultTable">'+tableHead+tableBody+'</table>'
          
               
          file.write('<div id="SecModelOverview"></div>')
          file.write('''<script type="text/javascript">

(function($){ // encapsulate jQuery

$(function () {''')
          file.write("$('#SecModelOverview').highcharts({")
          file.write('''
            chart: {
                type: 'bar'
            },
            title: {
                text: 'Security-Model-Overview Real-Issues',
                style : {
                        fontSize : '20px'
                    }
            },
            xAxis: {''')
          file.write(categories)
          
          #      categories: ['Total Issues', 'Oranges', 'Pears', 'Grapes', 'Bananas']
          file.write('''
           , labels : {
               style : {
                        fontSize : '18px'
                    }
           } },
            yAxis: {
                min: 0,
                stackLabels: {
                    enabled: true,
                    style: {
                        fontWeight: 'bold',
                        color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                    }
                },
                labels : {
                    style : {
                        fontSize : '18px'
                    }
                }
            },
            legend: {
                align: 'right',
                x: -100,
                verticalAlign: 'top',
                y: 20,
                floating: true,
                backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColorSolid) || 'white',
                borderColor: '#CCC',
                borderWidth: 1,
                shadow: false,
                itemStyle : {
                        fontSize : '18px'
                    }
            },
            tooltip: {
                formatter: function() {
                    return '<b>'+ this.x +'</b><br/>'+
                        this.series.name +': '+ this.y +'<br/>'+
                        'Total: '+ this.point.stackTotal;
                }
            },
            plotOptions: {
                column: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: true,
                        color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
                    }
                },
                series : {
                    pointPadding : 0.1,
                    groupPadding : 0.1
                }
            },''')
          file.write(seriesElem)
          file.write('''
            
        });
    });
    

})(jQuery);
</script>''')
          file.write(htmlTable)     
          
          
          
      def buildOverallSummary(self, file):
          #secIssues = self.securityModelResultMap[scannerName]
          
          
          
          
          containerId="secmodel_overall_summary"
          categories = "categories: ["
          corrLineMatch="{name: 'correct line matches', data: ["
          diffLineMath="{name: 'different line matches', data: ["
          rangeMatch="{name: 'range matches', data: ["
          diffTypeMatch="{name: 'different type matches', data: ["
          noneMatch="{name: 'none matching', data: ["
          
          firstRun = True
          for scannerName, secIssues in self.securityModelResultMap.items():
              compareResultMap = secIssues.compare()
              
              if(not firstRun):
                 
                  corrLineMatch+=", "
                  diffLineMath+=", "
                  rangeMatch+=", "
                  diffTypeMatch+=", "
                  noneMatch+=", "
                  categories+=", "
              firstRun = False
              categories+="'"+scannerName+"'"
              
              corrLineMatchCnt=0
              diffLineMathCnt = 0
              rangeMatchCnt = 0
              diffTypeMatchCnt = 0
              noneMatchCnt = 0
          #detailTable='<table class="defaultTable"><tr><td>Class</td><td>correct line matches</td><td>different line matches</td><td>range matches</td><td>different type matches</td><td>none matching</td></tr>'
          
              for weaknessClass, resultHolder in compareResultMap.items():
                  
                  
                  
                  
                  corrLineMatchCnt+=resultHolder.correctMatchCnt
                  diffLineMathCnt+=resultHolder.differentLineMatches
                  rangeMatchCnt+=resultHolder.rangeMatch
                  diffTypeMatchCnt+=resultHolder.differentTypeMatches
                  noneMatchCnt+=resultHolder.noneMatching
                  #detailTable+='<tr><td>'+weaknessClass+'</td><td>'+str(resultHolder.correctMatchCnt)+'</td><td>'+str(resultHolder.differentLineMatches)+'</td><td>'+str(resultHolder.rangeMatch)+'</td><td>'+str(resultHolder.differentTypeMatches)+'</td><td>'+str(resultHolder.noneMatching)+'</td></tr>'
              corrLineMatch+=str(corrLineMatchCnt)
              diffLineMath+=str(diffLineMathCnt)
              rangeMatch+=str(rangeMatchCnt)
              diffTypeMatch+=str(diffTypeMatchCnt)
              noneMatch+=str(noneMatchCnt)
              
          corrLineMatch+="]}"
          diffLineMath+="]}"
          rangeMatch+="]}"
          diffTypeMatch+="]}"
          noneMatch+="]}"
          categories+="]"
          
         # detailTable+='</table>'
          series = "series: ["+corrLineMatch+", "+diffLineMath+", "+rangeMatch+", "+diffTypeMatch+", "+noneMatch+"]"
                            
          file.write('<div id="'+containerId+'"></div>')
          file.write('''<script type="text/javascript">

(function($){ // encapsulate jQuery

$(function () {''')
          file.write("$('#"+containerId+"').highcharts({")
          file.write('''
            chart: {
                type: 'bar'
            },
            title: {
                text: 'Summary Issue distribution',
                style : {
                        fontSize : '20px'
                    }
            },
            xAxis: {''')
          file.write(categories)
          
          #      categories: ['Total Issues', 'Oranges', 'Pears', 'Grapes', 'Bananas']
          file.write('''
            ,labels : {
                    style : {
                        fontSize : '18px'
                    }
            }},
            yAxis: {
                min: 0,
                labels : {
                    style : {
                        fontSize : '18px'
                    }
                }
            },
            legend: {
               
                backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColorSolid) || 'white',
                borderColor: '#CCC',
                borderWidth: 1,
                shadow: false,
                itemStyle : {
                        fontSize : '18px'
                    }
            },
            tooltip: {
                formatter: function() {
                    return '<b>'+ this.x +'</b><br/>'+
                        this.series.name +': '+ this.y +'<br/>'+
                        'Total: '+ this.point.stackTotal;
                }
            },
            plotOptions: {
                series: {
                    stacking: 'normal',
                    
                    pointPadding : 0.1,
                    groupPadding : 0.1
                }
            
            
            },''')
          file.write(series)
          file.write('''
            
        });
    });
    

})(jQuery);
</script>''')
          #file.write(detailTable)
      
      def printLegend(self, file):
         file.write('<div id="legend" class="detailMain">')
         file.write("<h3>Legend</h3>")
         file.write('<table class="defaultTable">')
         file.write('<tr><td>Type</td><td>Description</td></tr>')
         file.write('<tr><td>correct line match</td><td>Issues of correct type found at correct line</td></tr>')
         file.write('<tr><td>different line</td><td>Issues of correct type found at a different line</td></tr>')
         file.write('<tr><td>range match</td><td>Issues of correct type found within a defined range</td></tr>')
         file.write('<tr><td>different type match</td><td>Issues of false type found at correct line</td></tr>')
         file.write('<tr><td>none matching</td><td>An Issues was found which is not documented in the testsuite</td></tr>')
         file.write('<tr><td>real issues</td><td>Number of issues which are found in files where also Juliet-Testsuite Issues are documented</td></tr>')
         file.write('<tr><td>other issues</td><td>Issues found in files where no Issues should be found</td></tr>')
         file.write('</table>')
         file.write('</div>')
      def buildReport(self):
          file = open(self.outputFilePath, "w")
          self.buildHTMLHead(file)
          self.buildBody(file)
          
          
          
          file.write("</html>")
          