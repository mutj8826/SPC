-- ดึงงานค้างวางแผน + ขั้นตอนแรก (Step_No = '10') จาก ENPRO (ฐาน ENPDS06-01)
-- ผลลัพธ์ 1 แถว = 1 SO, 21 ช่อง คั่นด้วย ~|~  → บันทึกทั้งหมดเป็น data/rows.txt (1 บรรทัดต่อ 1 แถว)
-- เปลี่ยนวันที่ใน WHERE ให้ครอบคลุมงานล่าสุดที่ต้องการ (ไม่ต้องดึงย้อนหลังเก่า)
SELECT
 ISNULL(p.SO_No,'')+'~|~'+
 ISNULL(CONVERT(varchar(10),p.SO_Date,23),'')+'~|~'+
 ISNULL(p.Customer_Name,'')+'~|~'+
 ISNULL(p.Job_Name,'')+'~|~'+
 ISNULL(CAST(p.Order_Qty AS varchar(20)),'')+'~|~'+
 ISNULL(CAST(p.DC_Answer_Qty AS varchar(20)),'')+'~|~'+
 ISNULL(CONVERT(varchar(10),p.DC_Receive_Date,23),'')+'~|~'+
 ISNULL(p.DC_Receive_Time_From,'')+'~|~'+
 ISNULL(p.DC_Receive_Time_To,'')+'~|~'+
 ISNULL(CONVERT(varchar(10),p.Customer_Ship_Date,23),'')+'~|~'+
 ISNULL(p.Customer_Ship_Time,'')+'~|~'+
 ISNULL(CONVERT(varchar(10),p.PN_Planned_Send_Date,23),'')+'~|~'+
 ISNULL(p.PN_Planned_Send_Time,'')+'~|~'+
 ISNULL(p.PN_Pending_Status,'')+'~|~'+
 ISNULL(s.Step_Atb,'')+'~|~'+
 ISNULL(s.Step_Short_Name,'')+'~|~'+
 ISNULL(s.Plan_Machine,'')+'~|~'+
 ISNULL(REPLACE(s.Plan_Start_Date,'/','-')+' '+s.Plan_Start_Time,'')+'~|~'+
 ISNULL(REPLACE(s.Plan_Finish_Date,'/','-')+' '+s.Plan_Finish_Time,'')+'~|~'+
 ISNULL(CONVERT(varchar(10),s.Plan_Send_Date,23),'')+'~|~'+
 ISNULL(CAST(s.Is_Planned AS varchar(3)),'0') AS line
FROM dbo.vw_EDoc_PN_Pending p
LEFT JOIN dbo.vw_EDoc_SO_Steps s ON s.SO_No = p.SO_No AND s.Step_No = '10'
WHERE p.SO_Date >= '2026-11-01'
ORDER BY p.SO_No;
