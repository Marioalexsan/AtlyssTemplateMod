using HarmonyLib;
using UnityEngine;

namespace TemplateMod.HarmonyPatches;

[HarmonyPatch(typeof(MainMenuManager), nameof(MainMenuManager.Set_MenuCondition))]
public static class MenuPatch
{
    [HarmonyPostfix]
    private static void SetMenuConditionPatch(MainMenuManager __instance)
    {
        __instance._versionDisplayText.text = Application.version + " with Mods :D";
    }
}