REM  *****  BASIC  *****

Sub CreateGraphs()
	sheetsCount = ThisComponent.getSheets().Count
	dim jump as boolean
	for s = 0 to sheetsCount-2
		oSheet = ThisComponent.Sheets.getByIndex(s)
		oCharts = oSheet.getCharts()
		for rng = 0 to 2
		jump = False
			gName = ""
			if rng = 0 then
				gName = oSheet.GetName + "_one_shot"
				end_row = findRow(oSheet,"BM")
				graph_data = oSheet.getCellRangeByName("BM3:BQ"+Trim(Str(end_row-1))).getRangeAddress()
				error_bar_range1 = "'"+oSheet.CodeName + "'" + ".BN3:" + "'" + oSheet.CodeName +"'"+ ".BN" + max_col
				error_bar_range2 = "'"+oSheet.CodeName + "'" + ".BQ3:" + "'" + oSheet.CodeName +"'"+ ".BQ" + max_col
				if end_row = 3 then
					jump = True
				endif
			endif
			if rng = 1 then
				gName = oSheet.GetName + "_CoT"
				end_row = findRow(oSheet,"BS")
				graph_data = oSheet.getCellRangeByName("BS3:BW"+Trim(Str(end_row-1))).getRangeAddress()
				error_bar_range1 = "'"+oSheet.CodeName + "'" + ".BT3:" + "'" + oSheet.CodeName +"'"+ ".BT" + max_col
				error_bar_range2 = "'"+oSheet.CodeName + "'" + ".BW3:" + "'" + oSheet.CodeName +"'"+ ".BW" + max_col
				if end_row = 3 then
					jump = True
				endif
			endif
			if rng = 2 then
				gName = oSheet.GetName + "_PoT"
				end_row = findRow(oSheet,"BY")
				graph_data = oSheet.getCellRangeByName("BY3:CC"+Trim(Str(end_row-1))).getRangeAddress()
				error_bar_range1 = "'"+oSheet.CodeName + "'" + ".BZ3:" + "'" + oSheet.CodeName +"'"+ ".BZ" + max_col
				error_bar_range2 = "'"+oSheet.CodeName + "'" + ".CC3:" + "'" + oSheet.CodeName +"'"+ ".CC" + max_col
				if end_row = 3 then
					jump = True
				endif
			endif
			if not jump then
				oRect = createObject("com.sun.star.awt.Rectangle")
				oRect.X = 1000
				oRect.Y = 1000
				oRect.width = 60000
				oRect.Height= 40000
				' True indicates that column headings should be used.
				' False indicates that Row headings should not be used.
				oCharts.addNewByName(gName, oRect, Array(graph_data), False, False)
				chart = oCharts.getByName(gName).EmbeddedObject
				chart.Title.String = gName
				chart.Diagram.stacked = True
				tmpRow = chart.Diagram.getDataRowProperties(0)
				tmpRow.FillStyle = 0
				tmpRow = chart.Diagram.getDataRowProperties(1)
				tmpRow.FillStyle = 0
				tmpRow.ErrorBarRangeNegative = error_bar_range1
				tmpRow.ErrorBarStyle = 7
				tmpRow.ErrorIndicator = 3
				tmpRow.DataErrorProperties.LineWidth = 60
				tmpRow.DataErrorProperties.ShowNegativeError = True
				tmpRow.DataErrorProperties.ShowPositiveError = False
				tmpRow = chart.Diagram.getDataRowProperties(3)
				tmpRow.ErrorBarRangePositive = error_bar_range2
				tmpRow.ErrorBarStyle = 7
				tmpRow.ErrorIndicator = 3
				tmpRow.DataErrorProperties.LineWidth = 60
				tmpRow.DataErrorProperties.ShowNegativeError = False
				tmpRow.DataErrorProperties.ShowPositiveError = True
				tmpRow = chart.Diagram.getDataRowProperties(4)
				tmpRow.FillStyle = 0
			endif
		next rng
	next s
End Sub

public function findRow(oSheet as object, column as String) as Integer
	dim cell as object 
	dim tmp as String
	findRow = 2
	do
		findRow = findRow + 1
		tmp = column + Trim(Str(findRow))
		cell = oSheet.getCellRangeByName(tmp)
	loop while cell.Formula <> "" and cell.String <> "No Value"
End Function

