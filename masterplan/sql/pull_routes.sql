-- ดึงเส้นทางผลิต (routing) ทุกขั้นตอนของงานชุดเดียวกับ pull_jobs.sql
-- ผลลัพธ์ 1 แถว = SO~|~เส้นทาง (คั่นขั้นด้วย +>)~|~จำนวนขั้น  → บันทึกเป็น data/routes.txt
-- ใช้วันที่เดียวกับ pull_jobs.sql
SELECT ISNULL(SO_No,'') + '~|~' + ISNULL(CAST(Routing_Path AS varchar(500)),'') + '~|~' + ISNULL(CAST(Steps_Total AS varchar(10)),'') AS line
FROM dbo.vw_EDoc_SO_Steps_Summary
WHERE SO_No IN (SELECT SO_No FROM dbo.vw_EDoc_PN_Pending WHERE SO_Date >= '2026-11-01')
ORDER BY SO_No;
