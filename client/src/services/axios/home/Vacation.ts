import type { eventNameType, userType, vacationItemType } from "./types"
import { v4 as uuidv4 } from "uuid";

class Vacation {

    // to create the vacations list
    public vacationsItems(eventName: eventNameType, vacations: any, date: Date): vacationItemType[] {
        let items: vacationItemType[] = [];
        for (const vacation of vacations) {
            items.push(this.vacationItem(eventName, vacation, date));
        }
        return items;
    }

    // subtracte 2 dates from eachother
    private subtractDates(date1: Date, date2: Date): number {
        return Math.abs(date1.getTime() - date2.getTime());
    }
    // add number to current date to get the end date of the vacation
    private endDays(): [Date, Date] {
        const today = new Date();
        const firstDay = new Date(today.setDate(today.getDate() - today.getDay()));
        const lastDay = new Date(today.setDate(today.getDate() - today.getDay() + 6));

        return [firstDay, lastDay];
    }




    // to create the vacation item
    private vacationItem(eventName: eventNameType, vacation: any, date: Date): vacationItemType {
        const id: string = uuidv4();

        const applying_user: userType = {
            id: vacation.applying_user.id,
            full_name: vacation.applying_user.full_name,
            email: vacation.applying_user.email,
            image: vacation.applying_user.image,
            team: vacation.applying_user.team,
            gender: vacation.applying_user.gender
        }
        const approval_user: userType = {
            id: vacation.approval_user.id,
            full_name: vacation.approval_user.full_name,
            email: vacation.approval_user.email,
            image: vacation.approval_user.image,
            team: vacation.approval_user.team,
            gender: vacation.approval_user.gender
        }
        console.log("event", vacation);
        let [from_year, from_month, from_day] = (vacation.from_date).split("-");
        let from_date = new Date(from_year, from_month, from_day);
        let [endYear, endMonth, endDay] = (vacation.end_date).split("-");
        let end_date = new Date(endYear, endMonth, endDay);
        let length = this.subtractDates(from_date, end_date) / (1000 * 3600 * 24);

        const [firstDay, lastDay] = this.endDays();
        /*   let start = this.subtractDates(from_date, firstDay) / (1000 * 3600 * 24);
          let end = this.subtractDates(end_date, lastDay) / (1000 * 3600 * 24);
   */
        /*         alert("from : " + from_date.getDate());
                alert("end : " + end_date.getDate());
                 */
        let start = from_date.getDate() - firstDay.getDate();
        let end = lastDay.getDate() - end_date.getDate();
        /*      alert("start : " + start);
             alert("end : " + end);
      */

        return {
            id: id,
            title: "🌴" + eventName,
            reason: vacation.reason,
            len: 1,
            applying_user: applying_user,
            approval_user: approval_user,
            status: vacation.status,
            date: date,
            className: "task--warning",
            eventName: eventName,
            isStart: true,
            isBottom: false,

        }
    }
}


export default Vacation;