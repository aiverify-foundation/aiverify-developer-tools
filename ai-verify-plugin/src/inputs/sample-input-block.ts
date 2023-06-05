/**
 * Input Block Summary functions. The below functions will be called by the AI Verify portal to get the summary and status of the Input Block data.
 */

/**
 * Return summary of data
 */
export function summary(data: any): string {
  // TODO: replace below code with meaningful summary of data.
  if (!data)
    return "No data";
  return JSON.stringify(data || {})
}

/**
 * Return progress in percentage (0-100). 100% will be refected as completed in the Input Progress list.
 */
export function progress(data: any): number {
  // TODO: replace below code with percentage of user completion.
  if (!data)
    return 0;
  const totalKeys = 3;
  const numKeys = Object.values(data).filter(v => {
    if (typeof (v) === "string" || Array.isArray(v)) {
      return v.length > 0;
    } else {
      return true;
    }
  }).length;
  return Math.round((numKeys / totalKeys) * 100);
}

/**
 * Return whether the data is valid. If data validation is not required, just return true.
 */
export function validate(data: any): boolean {
  // TODO: replace below code with data validation. 
  return progress(data) == 100;
}
