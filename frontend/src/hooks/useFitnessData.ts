import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import type { MeasurementRequest } from '../types/models'
import {
  createMeasurement,
  getActivities,
  getCenters,
  getGrowth,
  deleteMeasurement,
  getMeasurement,
  getMeasurements,
  createChild,
  getChildren,
  getRegionalInsight,
  getRegionalMap,
  updateChild,
} from '../api/resources'

export function useSaveChild() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (input: { childId?: string; nickname: string; gender: 'MALE' | 'FEMALE'; birthYearMonth: string }) => {
      const { childId, nickname, gender, birthYearMonth } = input
      return childId
        ? updateChild(childId, { nickname, gender, birthYearMonth })
        : createChild({ nickname, gender, birthYearMonth })
    },
    onSuccess: (child) => {
      queryClient.setQueryData(['children'], [child])
    },
  })
}
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

export const useActivities = (params: { fitnessElement?: string; measurementId?: string } = {}) =>
  useQuery({ queryKey: ['activities', params], queryFn: () => getActivities(params) })
export const useCenters = (
  params: { lat?: number; lng?: number; radiusKm?: number; sido?: string; sidoSigungu?: string } = {},
) => useQuery({ queryKey: ['centers', params], queryFn: () => getCenters(params) })
export function useCreateMeasurement() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (input: { childId: string; request: MeasurementRequest }) =>
      createMeasurement(input.childId, input.request),
    onSuccess: (_result, variables) => {
      queryClient.invalidateQueries({ queryKey: ['measurements', variables.childId] })
      queryClient.invalidateQueries({ queryKey: ['growth', variables.childId] })
    },
  })
}
export function useDeleteMeasurement() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (input: { measurementId: string; childId?: string }) => deleteMeasurement(input.measurementId),
    onSuccess: (_result, variables) => {
      if (variables.childId) queryClient.invalidateQueries({ queryKey: ['measurements', variables.childId] })
      queryClient.removeQueries({ queryKey: ['measurement', variables.measurementId] })
    },
  })
}

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
