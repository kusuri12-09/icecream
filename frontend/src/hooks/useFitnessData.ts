import { useQuery } from '@tanstack/react-query'
import {
  getActivities,
  getCenters,
  getGrowth,
  getMeasurement,
  getMeasurements,
  getChildren,
  getRegionalInsight,
  getRegionalMap,
} from '../api/resources'

export const useChildren = () => useQuery({ queryKey: ['children'], queryFn: getChildren })

export const useChild = () =>
  useQuery({
    queryKey: ['children'],
    queryFn: getChildren,
    select: (children) => children[0] ?? null,
  })

export const useRecords = () => {
  const childQuery = useChild()
  const recordsQuery = useQuery({
    queryKey: ['measurements', childQuery.data?.id],
    queryFn: () => getMeasurements(childQuery.data!.id),
    enabled: Boolean(childQuery.data?.id),
  })
  return { ...recordsQuery, isLoading: childQuery.isLoading || recordsQuery.isLoading }
}

export const useActivities = () => useQuery({ queryKey: ['activities'], queryFn: getActivities })
export const useCenters = () => useQuery({ queryKey: ['centers'], queryFn: getCenters })
export const useMeasurement = (measurementId?: string) =>
  useQuery({
    queryKey: ['measurement', measurementId],
    queryFn: () => getMeasurement(measurementId!),
    enabled: Boolean(measurementId),
  })
export const useGrowth = (childId?: string, itemKey?: string) =>
  useQuery({
    queryKey: ['growth', childId, itemKey],
    queryFn: () => getGrowth(childId!, itemKey),
    enabled: Boolean(childId),
  })
export const useRegionalInsight = (sidoSigungu?: string) =>
  useQuery({ queryKey: ['regional-insight', sidoSigungu], queryFn: () => getRegionalInsight(sidoSigungu) })
export const useRegionalMap = () => useQuery({ queryKey: ['regional-map'], queryFn: getRegionalMap })