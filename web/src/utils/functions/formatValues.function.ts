export function formatValues(
  value: number,
  type: 'decimal' | 'currency' | 'percent' = 'decimal'
): string {
  const options: Record<string, Intl.NumberFormatOptions> = {
    decimal: {
      style: 'decimal',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    },
    currency: { style: 'currency', currency: 'BRL' },
    percent: {
      style: 'percent',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    },
  };

  return value.toLocaleString('pt-BR', options[type] || options.decimal);
}
