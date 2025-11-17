/* InfluxDB query used to get the data:
SELECT 
  last("Fan1_on") as Fan1_On, 
  last("Fan2_on") as Fan2_On,  
  last("Fan1_off") as Fan1_Off, 
  last("Fan2_off") as Fan2_Off,  
  last("Fan_Speed") as FanSpeed_RPM,
  last("FeedbackPipeWatchdog") as FeedbackPipeWatchdog,
  last("Feedback_K1") as Feedback_K1,
  last("Feedback_K2") as Feedback_K2,
  last("Fuse_Dryer") as Fuse_Dryer,
  last("Fuse_Fan1") as Fuse_Fan1,
  last("Fuse_Fan2") as Fuse_Fan2,
  last("Inflation") as Inflation,
  last("No_Emergency") as NoEmergency,
  last("Operational_Hours_1") as OperationalHours1,
  last("Operational_Hours_2") as OperationalHours2,
  last("Pressure_Sensor") as Pressure,
  last("Set_Pressure") as SetPressure,
  last("Set_Pressure") as SetPressure,
  last("Set_Pressure_High") as SetPressure_High,
  last("Set_Pressure_Normal") as SetPressure_Normal,
  last("free") as free,
  last("low_press") as LowPressure
FROM "airflowm01" 
*/

options.debug = false; // Toggle for console.log statements
//console.log("Rendering airflowm01 SVG with data:", data);

const getFieldValue = (name) => data.series[0].fields.find(f => f.name === name).values[0];

options.statusData = {  
  "Fan1_On": getFieldValue("Fan1_On"),
  "Fan2_On": getFieldValue("Fan2_On"),
  "FanSpeed_RPM": getFieldValue("FanSpeed_RPM"),
  "FeedbackPipeWatchdog": getFieldValue("FeedbackPipeWatchdog"),
  "Feedback_K1": getFieldValue("Feedback_K1"),
  "Feedback_K2": getFieldValue("Feedback_K2"),
  "Fuse_Dryer": getFieldValue("Fuse_Dryer"),
  "Fuse_Fan1": getFieldValue("Fuse_Fan1"),
  "Fuse_Fan2": getFieldValue("Fuse_Fan2"),
  "Inflation": getFieldValue("Inflation"),
  "NoEmergency": getFieldValue("NoEmergency"),
  "OperationalHours1": getFieldValue("OperationalHours1"),
  "OperationalHours2": getFieldValue("OperationalHours2"),
  "Pressure": getFieldValue("Pressure"),
  "SetPressure": getFieldValue("SetPressure"),
  "SetPressure_High": getFieldValue("SetPressure_High"),
  "SetPressure_Normal": getFieldValue("SetPressure_Normal"),
  "free": getFieldValue("free"),
  "LowPressure": getFieldValue("LowPressure"),
  "SetPressure_Low": 100
};

options.statusMap = {
  'status-Fuse_Fan1': options.statusData['Fan1_On'] ? options.statusData['Fuse_Fan1'] : -1,
  'status-Feedback_K1': options.statusData['Fan1_On'] ? options.statusData['Feedback_K1'] : -1,
  'status-Fuse_Fan2': options.statusData['Fan2_On'] ? options.statusData['Fuse_Fan2'] : -1,
  'status-Feedback_K2': options.statusData['Fan2_On'] ? options.statusData['Feedback_K2'] : -1,
  'status-Inflation': options.statusData['Inflation'],
  'status-free': options.statusData['free'],
  'status-Fuse_Dryer': options.statusData['Fuse_Dryer'],
  'status-FeedbackPipeWatchdog': options.statusData['FeedbackPipeWatchdog']
};
  
svgmap.fan1Hours.text((options.statusData["OperationalHours1"]).toString().padStart(6, '0'));  
svgmap.fan2Hours.text((options.statusData["OperationalHours2"]).toString().padStart(6, '0'));    
    
options.updateRPMGauge(svgmap);
options.updatePressureGauge(svgmap);
options.updatePressureGaugeSegments(svgmap);  

options.updateStatuses(svgmap);
options.updateExhaust(svgmap);

// Click handlers for interactive elements
svgmap.statusFuseDryer.click(function () {
  options.log("Clicked fuse dryer");
  const newPressure = Math.round(options.statusData["Pressure"] - 69);
  svgmap.pressureValue.text(newPressure.toString());

  options.updatePressureGauge(svgmap);
});

svgmap.statusFuseFan2.click(function () {
  options.log("Clicked fuse fan2");

  const newSpeed = Math.round(options.statusData["FanSpeed_RPM"] + 100);
  svgmap.fanspeedValue.text(newSpeed.toString());

  options.updateRPMGauge(svgmap);
});

svgmap.statusFuseFan1.click(function () {
  options.log("Clicked fuse fan1");
  
  if (options.statusData["SetPressure_Low"] > 150) {
    options.statusData["SetPressure_Low"] = 100
  } else {
    options.statusData["SetPressure_Low"] = 150
  }

  options.updatePressureGaugeSegments(svgmap);

  options.log("Updated pressure labels and segments for new config");
  options.log(svgmap.pressureLowLabel.text());
});

svgmap.statusFeedbackK1.click(function () {
  options.log("Clicked feedback K1");

  svgmap.fan1Hours.text((options.statusData["OperationalHours1"] + 100).toString().padStart(6, '0'));
});

svgmap.statusFeedbackK2.click(function () {
  options.log("Clicked feedback K2");
  svgmap.fan2Hours.text((options.statusData["OperationalHours2"] + 100).toString().padStart(6, '0'));
});

svgmap.powerFan1Container.click(function () {
  options.log("Clicked fan1");
  options.statusData["Fan1_On"] = 1 - options.statusData["Fan1_On"];

  options.updateStatuses(svgmap);
  options.updateExhaust(svgmap);
});

svgmap.powerFan2Container.click(function () {
  options.log("Clicked fan2");
  options.statusData["Fan2_On"] = 1 - options.statusData["Fan2_On"];

  options.updateStatuses(svgmap);
  options.updateExhaust(svgmap);
});

svgmap.statusFeedbackPipeWatchdog.click(function () {
  options.log("Clicked watchdog");
  options.statusData["NoEmergency"] = 1 - options.statusData["NoEmergency"];

  options.updateStatuses(svgmap);
});
