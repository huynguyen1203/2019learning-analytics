library(tidyverse)
library(data.table)

# clean data ----
# keep courses provided on the UBC campus, and filter out graduate courses
# also remove problematic data (e.g. negative numbers in #registered)
df <- read_csv("C:\\Users\\Huy/ubc_course_calendar_data.csv") %>% 
  filter(CAMPUS == "UBC", !(COURSE_TITLE %like% "MASTERS"), !(COURSE_TITLE %like% "DOCTORAL"),
         !(COURSE_TITLE %like% "THESIS"), !is.na(START_TIME), CURRENTLY_REGISTERED >= 0,
         SECTION_TYPE != "W-L") %>%
  select(session = SESSION_YEAR, term = TERM,
         subject = SUBJECT_CODE, course_num = COURSE_NUMBER,
         section_num = SECTION_NUMBER, course = COURSE_TITLE,
         remaining_total = TOTAL_SEATS_REMAINING,
         curr_registered = CURRENTLY_REGISTERED) %>% 
  mutate(year = str_remove(session, "W|S"),
         id = str_c(subject, course_num, section_num, sep = " "),
         reg_capacity = if_else(remaining_total < 0, 1, 
                            curr_registered / (remaining_total + curr_registered)),
         over_capacity = if_else(remaining_total < 0, abs(remaining_total), 0)) %>% 
  distinct()

# function to display historical enrolment for a course
plot_capacity <- function(x) {
  ggplot(df %>% filter(id == x), aes(year, reg_capacity)) +
    geom_col(width = 0.7, fill = "royalblue") +
    geom_hline(size = 1.5, yintercept = 1, colour = "red", linetype = "dashed") +
    labs(x = "Year", y = "Enrolment Capacity", title = x) +
    theme(plot.title = element_text(size = 22, face = "bold", hjust = 0.5),
          panel.background = element_rect(fill = "white", colour = "black"),
          panel.grid.major.y = element_line(linetype = "dashed", colour = "gainsboro"),
          axis.title = element_text(size = 18, face = "bold"),
          axis.text = element_text(size = 16))
}

# examples
plot_capacity("NURS 337 434")
plot_capacity("PATH 404 1")
