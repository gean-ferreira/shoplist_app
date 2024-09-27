export function filterByKey<T>(
  data: T[],
  key: keyof T,
  value: string | number
): T {
  const item = data.find((item) => item[key] === value);
  if (!item) {
    throw new Error(`Item with ${String(key)} equal to ${value} not found`);
  }
  return item;
}
