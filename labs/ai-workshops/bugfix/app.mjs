export function rankJobs(jobs) {
  return jobs.sort((a, b) => String(b.priority).localeCompare(String(a.priority)));
}
