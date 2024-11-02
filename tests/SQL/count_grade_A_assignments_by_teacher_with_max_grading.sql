SELECT teacher_id, COUNT(*) AS grade_A_count
FROM assignments
WHERE grade = 'A'
GROUP BY teacher_id
ORDER BY grade_A_count DESC
LIMIT 1;