from django.conf import settings
from .models import LogEntry
# Get the logger for your app
def has_missing_hyphens_or_two_segment_value(dataset, log_file_name):
    missing_hyphen_found = False
    prev_hyphen = True  # Assume there's a hyphen before the first value
    for i, value in enumerate(dataset):
        if value == "-":
            prev_hyphen = True
        elif not prev_hyphen:
            file_instance = LogEntry(
                message=f"{log_file_name} - Missing consecutive pair at index number {dataset[i-1]}"
            )
            file_instance.save()
            missing_hyphen_found = True
        else:
            prev_hyphen = False

        segments = value.split(".")
        if len(segments) == 2 and segments[-1] != "-":
            file_instance = LogEntry(
                message=f"{log_file_name} - Two-segment value at index number (subgroup level): {dataset[i]}"
            )
            file_instance.save()
            missing_hyphen_found = True

    # If the last element is not a hyphen, and the last value was not a hyphen, it's also a missing hyphen
    if dataset[0] == "-" and not prev_hyphen:
        file_instance = LogEntry(
                message=f"{log_file_name} - Present empty cell at index number {dataset[0]}"
            )
        file_instance.save()
        missing_hyphen_found = True

    # If the last element is not a hyphen, and the last value was not a hyphen, it's also a missing hyphen
    if dataset[-1] != "-" and not prev_hyphen:
        file_instance = LogEntry(
                message=f"{log_file_name} - Missing consecutive pair at index number {dataset[-1]}"
            )
        file_instance.save()
        missing_hyphen_found = True

    # Check for duplicates
    non_hyphens = [value for value in dataset if value != "-"]
    duplicates = {x for x in non_hyphens if non_hyphens.count(x) > 1}
    if duplicates:
        file_instance = LogEntry(
                message=f"{log_file_name} - Duplicates detected: {', '.join(duplicates)}"
            )
        file_instance.save()
        missing_hyphen_found = True

    return missing_hyphen_found

def other_log(dataset, ref=None, matching_words=None, exception=False, log_file_name=None):
    # Use the logger for logging messages
    if '-' in dataset:
        if ' ' in ref:
            key, _ = list(matching_words.items())[-2]
            file_instance = LogEntry(
                    message=f"{log_file_name} - Remove extra lines from result sheet below the reference no: {key}"
                )
            file_instance.save()
            return True
        file_instance = LogEntry(
                message=f"{log_file_name} - Missing word ids or Unneccessary Rows in result sheet at reference no(Word id): {ref} :    {key}"
            )
        file_instance.save()
        
        return True
    elif exception:
        file_instance = LogEntry(
                message=f"{log_file_name} - Check Reference no (Arabic team) in result sheet at reference no: {ref}"
            )
        file_instance.save()
        return True

    return False
