import React, { useState, useMemo, useCallback } from "react"
import { StyleSheet, Text, View } from "react-native"
import { CalendarList } from "react-native-calendars"
import axios from 'axios'

const baseURL = "http://localhost:3000"

const CalendarView = (props) => {

    const { userId, navigateToDate } = props

    const [markedDates, setMarkedDates] = React.useState(null);

    const createMarkedDateObject = (dates) => {
      const markedDatesObj = {}
      for (var i = 0; i < dates.length; i += 1) {
        const date = dates[i]
        markedDatesObj[date] = {marked: true}
      }

      console.log(markedDatesObj)
      setMarkedDates(markedDatesObj)
    }

    React.useEffect(() => {
        axios
        .post(`${baseURL}/get-entry-dates`, {
            user_id: userId
        })
        .then((response) => {
          if (response.status == 200) {
            createMarkedDateObject(response.data)
          }
        })
        .catch((error) => {
          console.log(error)
        });
      }, []);

  return (
    <CalendarList
    style={{borderRadius: 10, marginTop: '3%'}}
    // Initially visible month. Default = now
    markedDates={markedDates}
    // Max amount of months allowed to scroll to the past. Default = 50
    pastScrollRange={50}
    // Max amount of months allowed to scroll to the future. Default = 50
    futureScrollRange={50}
    // Handler which gets executed on day press. Default = undefined
    onDayPress={day => {
        console.log("Pressed", day)
        if (markedDates[day.dateString]) {
            console.log("inside")
            navigateToDate(day.dateString)
        }
    }}
    // Handler which gets executed on day long press. Default = undefined
    onDayLongPress={day => {
        console.log('selected day', day);
    }}
    // Month format in calendar title. Formatting values: http://arshaw.com/xdate/#Formatting
    // Handler which gets executed when visible month changes in calendar. Default = undefined
    onMonthChange={month => {
        console.log('month changed', month);
    }}

    // If firstDay=1 week starts from Monday. Note that dayNames and dayNamesShort should still start from Sunday
    firstDay={1}
    />
  )
}

const styles = StyleSheet.create({
  header: {
    flexDirection: "row",
    width: "100%",
    justifyContent: "space-between",
    marginTop: 10,
    marginBottom: 10
  },
  month: {
    marginLeft: 5
  },
  year: {
    marginRight: 5
  }
})

export default CalendarView
