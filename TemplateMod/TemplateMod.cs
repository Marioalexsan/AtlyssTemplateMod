using BepInEx;
using HarmonyLib;
using UnityEngine;

namespace TemplateMod;

[BepInPlugin(PluginInfo.GUID, PluginInfo.NAME, PluginInfo.VERSION)]
[HarmonyPatch(typeof(TemplateMod), MethodType.Constructor)]
public class TemplateMod : BaseUnityPlugin
{
    private readonly Harmony _harmony = new Harmony($"{PluginInfo.GUID}");

    public TemplateMod()
    {
        UnityEngine.Debug.Log($"{PluginInfo.NAME} constructed!");
    }

    private void Awake()
    {
        UnityEngine.Debug.Log($"{PluginInfo.NAME} patching!");
        _harmony.PatchAll();

        UnityEngine.Debug.Log($"Hello from {PluginInfo.NAME}!");
        UnityEngine.Debug.Log($"Application version is ${Application.version}.");
    }
}