import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import "react-big-calendar/lib/css/react-big-calendar.css";
import { format, parseISO, differenceInDays } from "date-fns";

const localizer = momentLocalizer(moment);

export default function Dashboard() {

  const [data, setData] = useState([]);
  const [monthlySpend, setMonthlySpend] = useState([]);
  const [calendarEvents, setCalendarEvents] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is logged in
    if (!localStorage.getItem("authToken")) {
      navigate("/");
      return;
    }


    // Fetch API data
    fetch("http://localhost:8007/api/subscriptions/",{
        method: "GET",
        headers: {
            "Authorization": `Basic ${localStorage.getItem("authToken")}`,
            "Content-Type": "application/json",
        },
        }

    ) // Replace with your real API
      .then((res) => {
      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }
      return res.json();
    })
      .then((result) => {

          console.log("API Data:", result); // Debugging: Check API response
        setData(result.results);
        // setMonthlySpend(result.monthly_spend);
        setCalendarEvents(
          result.results.map((record) => ({
            title: record.plan.service + " - " + record.plan.cost + " " + record.plan.currency,
            recursion: record.plan.recursion_type_display,
            cost: record.plan.cost,
            currency: record.plan.currency,
            start: parseISO(record.renewal_date),
            end: parseISO(record.renewal_date),
          }))
        );
      })
      .catch((error) => console.error("Error fetching data:", error));

    // Fetch API Monthly Expenses
    fetch("http://localhost:8007/api/subscriptions/monthly_expenses",{
        method: "GET",
        headers: {
            "Authorization": `Basic ${localStorage.getItem("authToken")}`,
            "Content-Type": "application/json",
        },
        }

    ) // Replace with your real API
      .then((res) => {
      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }
      return res.json();
    })
      .then((result) => {

          console.log("API Monthly Expenses:", result); // Debugging: Check API response
        setMonthlySpend(result.monthly_expenses);

      })
      .catch((error) => console.error("Error fetching data:", error));
  }, [navigate]);


  const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload; // Access the bar's data
    return (
      <div style={{
        background: "white",
        padding: "10px",
        border: "1px solid #ddd",
        borderRadius: "5px",
        boxShadow: "0px 2px 8px rgba(0, 0, 0, 0.2)",
      }}>
        <p><strong>Month:</strong> {data.month}</p>
        <p><strong>Total Spend:</strong> {data.spend} SAR</p>

        {data.breakdown && data.breakdown.length > 0 && (
          <>
            <p><strong>Breakdown:</strong></p>
            <ul style={{ paddingLeft: "15px" }}>
              {data.breakdown.map((item, index) => (
                <li key={index}>
                  {item.service}: {item.cost} SAR
                </li>
              ))}
            </ul>
          </>
        )}
      </div>
    );
  }
  return null;
};


  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>

      {/* Records Table */}
      <div className="table-container">
        <h2 className="table-title">Records</h2>
          <table className="table-bordered" style={{ textAlign: "center", justifyContent: "center", width: "100%"}}>
              <thead>
              <tr>
                  <th style={{textAlign: "center"}}>User</th>
                  <th style={{textAlign: "center"}}>Service</th>
                  <th style={{textAlign: "center"}}>Plan Type</th>
                  <th style={{textAlign: "center"}}>Renewal Date</th>
                  <th style={{textAlign: "center"}}>Switch to annual and save per year</th>
              </tr>
              </thead>
              <tbody>
              {data.map((record) => {
                  const renewalDate = new Date(record.renewal_date);
                  const daysUntilRenewal = differenceInDays(renewalDate, new Date());

                  // Check if renewal date is within the next 7 days
                  const isSoon = daysUntilRenewal > 0 && daysUntilRenewal <= 7;

                  return (
                      <tr key={record.id} className="border">
                          <td style={{ textAlign: "center" }}>{record.user}</td>
                          <td style={{textAlign: "center"}}>{record.plan.service}</td>
                          <td style={{textAlign: "center"}}>{record.plan.recursion_type_display}</td>
                          <td
                              style={{
                                  backgroundColor: isSoon ? "yellow" : "transparent", // ✅ Highlight only the renewal date
                                  fontWeight: isSoon ? "bold" : "normal",
                                  textAlign: "center",
                              }}
                          >
                              {format(renewalDate, "PPP")}
                          </td>
                          <td style={{textAlign: "center"}}>{record.switch_diff_month_to_annual}</td>
                      </tr>
                  );
              })}
              </tbody>
          </table>
      </div>

        {/* Monthly Spend Chart */}
        <div className="bg-white p-4 shadow rounded-lg mb-6">
            <h2 className="text-xl font-bold mb-4">Monthly Spend</h2>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={monthlySpend}>
                    <XAxis dataKey="month"/>
                    <YAxis/>
                    <Tooltip content={<CustomTooltip />}/>
                    <Bar dataKey="spend" fill="#4F46E5"/>
                </BarChart>
            </ResponsiveContainer>
        </div>

        {/* Calendar */}
        <div className="bg-white p-4 shadow rounded-lg">
            <h2 className="text-xl font-bold mb-4">Subscription Renewals</h2>
            <Calendar
                localizer={localizer}
                events={calendarEvents}
                startAccessor="start"
                endAccessor="end"
          style={{ height: 500 }}
        />
      </div>
    </div>
  );
}
