
options.debug = false; // Toggle for console.log statements

options.log = (...args) => {
  if (options.debug) console.log(...args);
};

options.statusData = {  
  "Fan1_On": 0,
  "Fan2_On": 0,
  "FanSpeed_RPM": 0,
  "FeedbackPipeWatchdog": 0,
  "Feedback_K1": 0,
  "Feedback_K2": 0,
  "Fuse_Dryer": 0,
  "Fuse_Fan1": 0,
  "Fuse_Fan2": 0,
  "Inflation": 0,
  "NoEmergency": 0,
  "OperationalHours1": 0,
  "OperationalHours2": 0,
  "Pressure": 0,
  "SetPressure": 0,
  "SetPressure_High": 0,
  "SetPressure_Normal": 0,
  "SetPressure_Low": 100,
  "free": 0,
  "LowPressure": 0
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

// Update status indicator element based on value
options.updateStatusElement = (el, value) => {
  options.log("Updating circle:", el, "with value:", value);
  if (value === 1) {
    el.fill('#00FF00');
    el.addClass('status-active');
  } else if (value === 0) {
    el.fill('#FF0000');
    el.addClass('status-active');
  } else {
    // Default/unknown state
    el.fill('gray');
    el.removeClass('status-active');
  }
}; 

// Update RPM gauge based on FanSpeed_RPM
options.updateRPMGauge = (svgmap) => {  
  const cx = 40; //parseFloat(gauge.getAttribute('data-cx'));
  const cy = 18; //parseFloat(gauge.getAttribute('data-cy'));
  const gaugeRadius = 15;
  const maxRPM = 4000;
  const gaugeStartAngle = 0; // 0°
  const gaugeEndAngle = Math.PI; // 180°
    
  const rpmValue = Math.round(options.statusData["FanSpeed_RPM"]); 
  svgmap.fanspeedValue.text(rpmValue.toString());  
  // Update value arc
  if (rpmValue >= 0) {
    const rpmRatio = Math.min(rpmValue / maxRPM, 1);
    const deltaAngle = rpmRatio * (gaugeEndAngle - gaugeStartAngle);
    
    // Start at rotated gauge start (gaugeStartAngle + π) and sweep by deltaAngle
    const valueStartAngle = gaugeStartAngle + Math.PI;
    const valueEndAngle = valueStartAngle + deltaAngle;
    const valueSweepFlag = 1;
    const valueAngleSpan = Math.abs(valueEndAngle - valueStartAngle);
    const valueLargeArc = (valueAngleSpan > Math.PI) ? 1 : 0;
    
    const startX = cx + gaugeRadius * Math.cos(valueStartAngle);
    const startY = cy + gaugeRadius * Math.sin(valueStartAngle);
    const endX = cx + gaugeRadius * Math.cos(valueEndAngle);
    const endY = cy + gaugeRadius * Math.sin(valueEndAngle);
    
    const arcPath = `M ${startX.toFixed(3)} ${startY.toFixed(3)} A ${gaugeRadius} ${gaugeRadius} 0 ${valueLargeArc} ${valueSweepFlag} ${endX.toFixed(3)} ${endY.toFixed(3)}`;
    svgmap.fanspeedValueArc.plot(arcPath);
    options.log("RPM value arc updated to:", arcPath);
  } else { 
    svgmap.fanspeedValueArc.plot('');
    options.log("RPM value arc cleared due to negative RPM value");
  }
  
  // Update indicator triangle
  if (rpmValue >= 0) {
    const rpmRatio = Math.min(rpmValue / maxRPM, 1);
    const indicatorAngle = gaugeStartAngle + (rpmRatio * (gaugeEndAngle - gaugeStartAngle));
    
    const indicatorRadius = gaugeRadius - 3;
    const triangleSize = 2.25;
    const baseRadius = indicatorRadius - triangleSize;
    const newTriangleHeight = triangleSize * 3;
    const tipRadius = baseRadius + newTriangleHeight;
    const halfShift = newTriangleHeight;
    const baseRadiusShifted = baseRadius - halfShift;
    const tipRadiusShifted = tipRadius - halfShift;
    
    let trianglePoints = [
      [cx + tipRadiusShifted * Math.cos(indicatorAngle), cy + tipRadiusShifted * Math.sin(indicatorAngle)],
      [cx + baseRadiusShifted * Math.cos(indicatorAngle - 0.2), cy + baseRadiusShifted * Math.sin(indicatorAngle - 0.2)],
      [cx + baseRadiusShifted * Math.cos(indicatorAngle + 0.2), cy + baseRadiusShifted * Math.sin(indicatorAngle + 0.2)]
    ];
    
    // Symmetric with respect to center (mirror)
    trianglePoints = trianglePoints.map(([px, py]) => [2 * cx - px, 2 * cy - py]);
     
    svgmap.fanspeedIndicator.plot(trianglePoints);
    options.log("RPM indicator updated to:", trianglePoints.map(p => p.join(',')).join(' '));
  } else { 
    svgmap.fanspeedIndicator.plot([[0,0],[0,0],[0,0]]);
    options.log("RPM indicator 0,0 0,0 0,0"); 
  }
}

// Update pressure gauge segments based on SetPressure_Low and SetPressure_High
options.updatePressureGaugeSegments = (svgmap) => {   
  const cx = 40; //parseFloat(gauge.getAttribute('data-cx'));
  const cy = -13; //parseFloat(gauge.getAttribute('data-cy'));
   
  const extraRadius2 = 30; // Radius for colored arc segments
  const maxPressure = 500;
  const gaugeStartAngle = -24.5 * Math.PI / 180; // -24.5°
  const gaugeEndAngle = Math.PI + 24.5 * Math.PI / 180; // 204.5°
  
  // Helper function to create arc path
  function createArcPath(startRatio, endRatio, radius) {
    const startAngle = gaugeStartAngle + startRatio * (gaugeEndAngle - gaugeStartAngle) + Math.PI;
    const endAngle = gaugeStartAngle + endRatio * (gaugeEndAngle - gaugeStartAngle) + Math.PI;
    const angleSpan = Math.abs(endAngle - startAngle);
    const largeArc = angleSpan > Math.PI ? 1 : 0;
    
    const startX = cx + radius * Math.cos(startAngle);
    const startY = cy + radius * Math.sin(startAngle);
    const endX = cx + radius * Math.cos(endAngle);
    const endY = cy + radius * Math.sin(endAngle);
    
    return {
      path: `M ${startX.toFixed(3)} ${startY.toFixed(3)} A ${radius} ${radius} 0 ${largeArc} 1 ${endX.toFixed(3)} ${endY.toFixed(3)}`,
      startAngle,
      endAngle
    };
  }
  const lowThreshold = options.statusData["SetPressure_Low"];
  const highThreshold = options.statusData["SetPressure_High"]; 
  const pressureYellowLowArcNew = createArcPath(lowThreshold / maxPressure, (lowThreshold + 50) / maxPressure, extraRadius2);
 
  svgmap.pressureYellowLowArc.plot(pressureYellowLowArcNew.path);
  options.log("Updated yellow-low arc to:", pressureYellowLowArcNew.path);
  
  
  const pressureLowArcNew = createArcPath(0, lowThreshold / maxPressure, extraRadius2);
  //svgmap.pressureLowArc.attr('d', pressureLowArcNew.path);
  svgmap.pressureLowArc.plot(pressureLowArcNew.path);
  options.log("Updated low arc to:", pressureLowArcNew.path);

  const greenStart = (lowThreshold + 50) / maxPressure;
  const greenEnd = highThreshold / maxPressure;
  const greenArcNew = createArcPath(greenStart, greenEnd, extraRadius2);
  //svgmap.pressureGreenArc.attr('d', greenArcNew.path);
  svgmap.pressureGreenArc.plot(greenArcNew.path);
  options.log("Updated green arc to:", greenArcNew.path); 

  const highStart = highThreshold / maxPressure;
  const pressureYellowHighArcNew = createArcPath(highStart, 1, extraRadius2);
  //svgmap.pressureYellowHighArc.attr('d', pressureYellowHighArcNew.path);
  svgmap.pressureYellowHighArc.plot(pressureYellowHighArcNew.path);
  options.log("Updated yellow-high arc to:", pressureYellowHighArcNew.path);
   
  svgmap.pressureLowLabel.text(`LOW ${options.statusData["SetPressure_Low"]}`);
  svgmap.pressureNormalLabel.text(`NORMAL ${options.statusData["SetPressure_Normal"]}`);
  svgmap.pressureHighLabel.text(`HIGH ${options.statusData["SetPressure_High"]}`);
  svgmap.pressureSetLabel.text(`SET ${options.statusData["SetPressure"]}`);   
}
 
options.updatePressureGauge = (svgmap) => {
  
  const newPressure = Math.round(options.statusData["Pressure"]);
  options.log("Updating pressure gauge with value:", newPressure);
  
  //const gauge = svgmap.pressure;
  const cx = 40; //parseFloat(gauge.getAttribute('data-cx'));
  const cy = -13; //parseFloat(gauge.getAttribute('data-cy'));
  const gaugeRadius = 15;
  const maxPressure = 500;
  const gaugeStartAngle = -24.5 * Math.PI / 180; // -24.5°
  const gaugeEndAngle = Math.PI + 24.5 * Math.PI / 180; // 204.5°
  
  const pressureValueText = String(Math.max(0, Math.min(newPressure, maxPressure))); // Clamp to [0, maxPressure]  
  options.log("Updating pressure gauge with value:", pressureValueText);
  svgmap.pressureValue.text(pressureValueText);
  options.log("NEW pressure gauge with value:",  svgmap.pressureValue.text()); 
  // Update value arc
  if (newPressure >= 0) {
    const pressureRatio = Math.min(newPressure / maxPressure, 1);
    const deltaAngle = pressureRatio * (gaugeEndAngle - gaugeStartAngle);
    
    // Start at rotated gauge start (gaugeStartAngle + π) and sweep by deltaAngle
    const valueStartAngle = gaugeStartAngle + Math.PI;
    const valueEndAngle = valueStartAngle + deltaAngle;
    const valueSweepFlag = 1;
    const valueAngleSpan = Math.abs(valueEndAngle - valueStartAngle);
    const valueLargeArc = (valueAngleSpan > Math.PI) ? 1 : 0;
    
    const startX = cx + gaugeRadius * Math.cos(valueStartAngle);
    const startY = cy + gaugeRadius * Math.sin(valueStartAngle);
    const endX = cx + gaugeRadius * Math.cos(valueEndAngle);
    const endY = cy + gaugeRadius * Math.sin(valueEndAngle);
    
    const arcPath = `M ${startX.toFixed(3)} ${startY.toFixed(3)} A ${gaugeRadius} ${gaugeRadius} 0 ${valueLargeArc} ${valueSweepFlag} ${endX.toFixed(3)} ${endY.toFixed(3)}`;
    svgmap.pressureValueArc.attr('d', arcPath);
    options.log("Pressure value arc updated to:", arcPath);
    
    // Update color based on pressure ranges
    if (newPressure < 100) {
      svgmap.pressureValueArc.style.stroke = '#FF0000'; // Red
    } else if (newPressure < 150) {
      svgmap.pressureValueArc.style.stroke = '#FFFF00'; // Yellow 
    } else if (newPressure <= 350) {
      svgmap.pressureValueArc.style.stroke = '#00FF00'; // Green
    } else {
      svgmap.pressureValueArc.style.stroke = '#FFFF00'; // Yellow
    }
  } else {
    svgmap.pressureValueArc.attr('d', '');
    options.log("Pressure value arc cleared due to negative pressure value"); 
  }
  
  // Update indicator triangle
  if (newPressure >= 0) { 
    const pressureRatio = Math.min(newPressure / maxPressure, 1);
    const indicatorAngle = gaugeStartAngle + (pressureRatio * (gaugeEndAngle - gaugeStartAngle));
    
    const indicatorRadius = gaugeRadius - 3;
    const triangleSize = 2.25;
    const baseRadius = indicatorRadius - triangleSize;
    const newTriangleHeight = triangleSize * 3;
    const tipRadius = baseRadius + newTriangleHeight;
    const halfShift = newTriangleHeight;
    const baseRadiusShifted = baseRadius - halfShift;
    const tipRadiusShifted = tipRadius - halfShift;
    
    let trianglePoints = [
      [cx + tipRadiusShifted * Math.cos(indicatorAngle), cy + tipRadiusShifted * Math.sin(indicatorAngle)],
      [cx + baseRadiusShifted * Math.cos(indicatorAngle - 0.2), cy + baseRadiusShifted * Math.sin(indicatorAngle - 0.2)],
      [cx + baseRadiusShifted * Math.cos(indicatorAngle + 0.2), cy + baseRadiusShifted * Math.sin(indicatorAngle + 0.2)]
    ];
    
    // Symmetric with respect to center (mirror)
    trianglePoints = trianglePoints.map(([px, py]) => [2 * cx - px, 2 * cy - py]);    
    svgmap.pressureIndicator.plot(trianglePoints);
    const points = trianglePoints.map(p => p.join(',')).join(' ');
    options.log("Pressure indicator updated to:", points);
  }
  
  // Update disk gradient based on low pressure 
  if (newPressure <= options.statusData["SetPressure_Low"]) {
    svgmap.pressureDiskPath.attr('fill', 'url(#red-gradient)');
    svgmap.pressure.addClass('pulsating-disk');    
  } else {
    svgmap.pressureDiskPath.attr('fill', 'url(#disk-gradient)');
    svgmap.pressure.removeClass('pulsating-disk');
  }
  options.log("Pressure disk gradient updated to:", newPressure <= options.statusData["SetPressure_Low"] ? 'url(#red-gradient)' : 'url(#disk-gradient)');

  // Update low pressure indicator visibility  
  if (newPressure <= options.statusData["SetPressure_Low"]) {
    svgmap.pressureLowPressureIndicator.attr('opacity', '1');
  } else {
    svgmap.pressureLowPressureIndicator.attr('opacity', '0');
  }
   options.log("Pressure low indicator opacity set to:", newPressure <= options.statusData["SetPressure_Low"] ? '1' : '0'); 
}
 
// Update status indicators based on statusData
options.updateStatuses = (svgmap) => {

  if (options.statusData["Fan1_On"] && !svgmap.powerFan1.hasClass('power-on'))
    svgmap.powerFan1.addClass('power-on')
  else if (!options.statusData["Fan1_On"] && svgmap.powerFan1.hasClass('power-on'))
    svgmap.powerFan1.removeClass('power-on')

  if (options.statusData["Fan2_On"] && !svgmap.powerFan2.hasClass('power-on'))
    svgmap.powerFan2.addClass('power-on')
  else if (!options.statusData["Fan2_On"] && svgmap.powerFan2.hasClass('power-on'))
    svgmap.powerFan2.removeClass('power-on') 
     
  // Update no-errors indicator  
  if (options.statusData["NoEmergency"] === 1) {
    svgmap.noErrorsDisc.attr('fill', 'green');
    svgmap.noErrorsDisc.addClass('status-active');
    svgmap.noErrorsSymbol.text('✓');
  } else {
    svgmap.noErrorsDisc.attr('fill', 'url(#status-red-gradient)');
    svgmap.noErrorsDisc.removeClass('status-active');
    svgmap.noErrorsSymbol.text('✗');
  }
      
  options.updateStatusElement(
    svgmap.statusFuseFan1,
    options.statusMap['status-Fuse_Fan1']
  );

  options.updateStatusElement(
    svgmap.statusFuseFan2,
    options.statusMap['status-Fuse_Fan2']
  );

  options.updateStatusElement(
    svgmap.statusFeedbackK1,
    options.statusMap['status-Feedback_K1']
  );

  options.updateStatusElement(
    svgmap.statusFeedbackK2,
    options.statusMap['status-Feedback_K2']
  );

  options.updateStatusElement(
    svgmap.statusFuseDryer,
    options.statusMap['status-Fuse_Dryer']
  );

  options.updateStatusElement(
    svgmap.statusFeedbackPipeWatchdog,
    options.statusMap['status-FeedbackPipeWatchdog']
  );
}
 
options.updateExhaust = (svgmap) => { 
  options.log("Updating exhaust visibility based on fan states");

  svgmap.exhaustContainer1.css('display', options.statusData["Fan1_On"] ? 'block' : 'none');  
  svgmap.exhaustContainer2.css('display', options.statusData["Fan2_On"] ? 'block' : 'none');
  svgmap.exhaustContainerCenter.css('display', (options.statusData["Fan1_On"] || options.statusData["Fan2_On"]) ? 'block' : 'none');
}


 